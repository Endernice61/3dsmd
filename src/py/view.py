import sys
import struct

###Read file name
try:
    source_file_input_string = sys.argv[1]
except:
    print("Please enter the file you would like read: ")
    source_file_input_string = input()

###Open input file
try:
    source_f = open(source_file_input_string,"rb")
except:
    print("File failed to open")
    exit()

def printd(indent,string,end="\n"):
    print("| "*indent+string,end=end)

def printn(indent,end="\n"):
    printd(indent,"+-+------------",end=end)

def printe(indent,end="\n"):
    printd(indent,"+--------------",end=end)

def read_chunk(f,size):
    if (size <= f.tell()): return
    chunk_id = int.from_bytes(f.read(2),byteorder='little')
    chunk_length = int.from_bytes(f.read(4),byteorder='little')
    #print(hex(chunk_id))
    #print(chunk_length)
    if (chunk_id == 0x4d4d):
        printe(0)
        printd(1,"MAIN CHUNK")
        printd(1,f"length = {chunk_length}")
        if (chunk_length > 6): read_chunk(f,size)
        printe(0)
    elif (chunk_id == 0x3d3d):
        printn(0)
        printd(2,"3D EDITOR CHUNK")
        printd(2,f"length = {chunk_length}")
        if (chunk_length > 6): read_chunk(f,size)
        printe(1)
    elif (chunk_id == 0x4000):
        printn(1)
        printd(3,"OBJECT BLOCK")
        printd(3,f"length = {chunk_length}")
        printd(3,"Object name = ",end="")
        char = f.read(1).decode()
        name = char
        read = 1
        while (char != '\0'):
            char = f.read(1).decode()
            name = name + char
            read = read + 1
        print(name)
        if (chunk_length > read+6): read_chunk(f,size)
        printe(2)
    elif (chunk_id == 0x4100):
        printn(2)
        printd(4,"TRIANGULAR MESH")
        printd(4,f"length = {chunk_length}")
        if (chunk_length > 6): read_chunk(f,size)
        printe(3)
    elif (chunk_id == 0x4110):
        printn(3)
        printd(5,"VERTICES LIST")
        printd(5,f"length = {chunk_length}")
        printd(5,"Vertices number = ",end="")
        data_length = int.from_bytes(f.read(2),byteorder='little')
        print(data_length)
        printd(5,"Vertices list = ",end="")
        #Learn how to link assembly and python
        vertices_read = 0
        while (vertices_read < data_length):
            if (vertices_read > 0): print(",",end="")
            print("[",
                  struct.unpack('<f',f.read(4))[0],
                  struct.unpack('<f',f.read(4))[0],
                  struct.unpack('<f',f.read(4))[0],
                  "]",end="")
            vertices_read += 1
        print()
        if (chunk_length > data_length*12+2+6): raise Exception("VERTICES LIST has extra length!")
        printe(4)
    elif (chunk_id == 0x4120):
        printn(3)
        printd(5,"FACES DESCRIPTION")
        printd(5,f"length = {chunk_length}")
        printd(5,"Polygons number = ",end="")
        data_length = int.from_bytes(f.read(2),byteorder='little')
        print(data_length)
        printd(5,"Polygons list = ",end="")
        #Learn how to link assembly and python
        polygons_read = 0
        while (polygons_read < data_length):
            if (polygons_read > 0): print(",",end="")
            print("[",
                  int.from_bytes(f.read(2),byteorder='little'),
                  int.from_bytes(f.read(2),byteorder='little'),
                  int.from_bytes(f.read(2),byteorder='little'),
                  "]",end="")
            polygons_read += 1
            f.read(2)
        print()
        if (chunk_length > data_length*8+2+6): read_chunk(f,size)
        printe(4)
    else:
        f.read(chunk_length-6)
    read_chunk(f,size)
    
###Read the file
source_f.seek(0,2)
size = source_f.tell()
source_f.seek(0,0)
read_chunk(source_f,size)
        

source_f.close()
