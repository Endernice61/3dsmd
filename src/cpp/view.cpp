#include <iostream>
#include <fstream>
#include <cstdlib>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <chrono>
#include "buffer.cpp"
#define DEBUG_CHUNK 0

const std::string BRANCH = "+-+------------";
const std::string LEAF = "+--------------";

std::string indents(int indent) {
	std::string out = "";
	for (;indent > 0;--indent) { out += "| "; }
	return out;
}

int read(std::ifstream& f, int c) {
	int ret = 0;
	for (int i = 0; i<c; ++i) {
		unsigned char byte = f.get();
		ret |= ((int)byte)<<(i*8);
	}
	return ret;
}

float readf(std::ifstream& f) {
	int ret = read(f,4);
	return *(float*)(&ret);
}

void read_chunk(Buffer& b,std::ifstream& f) {
	while (!f.eof()) {
		int chunk_id = read(f,2);
		if (f.eof()) { break; }//Off by one error correction
		int chunk_length = read(f,4);
		#if DEBUG_CHUNK
		std::cout << "Reading: " << chunk_id << " with length: " << chunk_length << '\n';
		#endif
		
		if (chunk_id == 0x4d4d) {
			b << LEAF << '\n';
			b << indents(1) << "MAIN CHUNK" << '\n';
			b << indents(1) << "length = " << chunk_length << '\n';
			if (chunk_length > 6) { read_chunk(b,f); }
			b << LEAF << '\n';
		} else if (chunk_id == 0x3d3d) {
			b << BRANCH << '\n';
			b << indents(2) << "3D EDITOR CHUNK" << '\n';
			b << indents(2) << "length = " << chunk_length << '\n';
			if (chunk_length > 6) { read_chunk(b,f); }
			b << indents(1) << LEAF << '\n';
		} else if (chunk_id == 0x4000) {
			b << indents(1) << BRANCH << '\n';
			b << indents(3) << "OBJECT BLOCK" << '\n';
			b << indents(3) << "length = " << chunk_length << '\n';
			b << indents(3) << "Object name = ";
			int read = 0;
			char name = f.get();
			read = 1;
			b << name;
			while (name != '\0') {
				name = f.get();
				b << name;
				++read;
			} b << '\n';
			if (chunk_length > read+6) { read_chunk(b,f); }
			b << indents(2) << LEAF << '\n';
		} else if (chunk_id == 0x4100) {
			b << indents(2) << BRANCH << '\n';
			b << indents(4) << "TRIANGULAR MESH" << '\n';
			b << indents(4) << "length = " << chunk_length << '\n';
			if (chunk_length > 6) { read_chunk(b,f); }
			b << indents(3) << LEAF << '\n';
		} else if (chunk_id == 0x4110) {
			b << indents(3) << BRANCH << '\n';
			b << indents(5) << "VERTICES LIST" << '\n';
			b << indents(5) << "length = " << chunk_length << '\n';
			b << indents(5) << "Vertices number = ";
			int data_length = read(f,2);
			b << data_length << '\n';
			b << indents(5) << "Vertices list = ";
			int vertices_read = 0;
			for (int vertices_read = 0; vertices_read < data_length; ++vertices_read) {
				if (vertices_read > 0) { b << ", "; }
				b << "[" << readf(f) << " " << readf(f) << " " << readf(f) << "]";
			}
			b << '\n';
			if (chunk_length > data_length*12+2+6) { throw "VERTICES LIST has extra length!"; }
			b << indents(4) << LEAF << '\n';
		} else if (chunk_id == 0x4120) {
			b << indents(3) << BRANCH << '\n';
			b << indents(5) << "FACES DESCRIPTION" << '\n';
			b << indents(5) << "length = " << chunk_length << '\n';
			b << indents(5) << "Polygons number = ";
			int data_length = read(f,2);
			b << data_length << '\n';
			b << indents(5) << "Polygons list = ";
			for (int polygons_read = 0; polygons_read < data_length; ++polygons_read) {
				if (polygons_read > 0) { b << ", "; }
				b << "[" << read(f,2) << " " << read(f,2) << " " << read(f,2) << "]";
				read(f,2);
			}
			b << '\n';
			if (chunk_length > data_length*8+2+6) { read_chunk(b,f); }
			b << indents(4) << LEAF << '\n';
		} else {
			f.seekg(chunk_length-6,std::ios::cur);
		}
	}
}

int main(int argv, char** argc) {
	//Read file name
	char* src_name;
	if (argv == 2) { src_name = argc[1]; } 
	else {
		std::cout << "Please enter the file you would like read: ";
		std::cin >> src_name;
	}
	
	std::ifstream file;
	file.open(src_name,std::ios::binary);
	if (!file.is_open()) {
		std::cout << "File failed to open";
		return 0;
	}
	
	//Read the file
	Buffer out = Buffer();
	read_chunk(out,file);
	std::cout << out.flush();
		
	file.close();
}
