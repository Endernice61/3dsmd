import sys
import struct
import read_matrix
import linear_transformation

###Read file name
try:
    source_file_input_string = sys.argv[1]
except:
    print("Please enter the file you would like transform: ")
    source_file_input_string = input()

###Open input file
try:
    source_f = open(source_file_input_string,"rb")
except:
    print("File failed to open")
    exit()

###Open output file + input file type check
try:
    out_f_string = source_file_input_string.replace(".3ds","_transformed.3ds")
    if (out_f_string == source_file_input_string): raise Exception()
    out_f = open(out_f_string,"wb")
except:
    print("The file is not a .3ds")
    source_f.close()
    exit()

###Read the matrix from the console
transformation = read_matrix.read_matrix()

def read_chunk(f,o,size):
    if (size <= f.tell()): return
    chunk_id = int.from_bytes(f.read(2),byteorder='little')
    chunk_length = int.from_bytes(f.read(4),byteorder='little')
    o.write(int.to_bytes(chunk_id,length=2,byteorder='little'))
    o.write(int.to_bytes(chunk_length,length=4,byteorder='little'))
    if (chunk_id == 0x4d4d): #Main chuck
        if (chunk_length > 6): read_chunk(f,o,size)
    elif (chunk_id == 0x3d3d):#3d Editor chunk
        if (chunk_length > 6): read_chunk(f,o,size)
    elif (chunk_id == 0x4000):#Object block
        char = f.read(1)
        o.write(char)
        read = 1
        while (char != b'\x00'):
            char = f.read(1)
            o.write(char)
            read = read + 1
        if (chunk_length > read+6): read_chunk(f,o,size)
    elif (chunk_id == 0x4100): #Triangular mesh
        if (chunk_length > 6): read_chunk(f,o,size)
    elif (chunk_id == 0x4110): #Vertices list
        data_length = int.from_bytes(f.read(2),byteorder='little')
        o.write(int.to_bytes(data_length,length=2,byteorder='little')) #Yes
        vertices_read = 0
        while (vertices_read < data_length):
            vec = [struct.unpack('<f',f.read(4))[0],struct.unpack('<f',f.read(4))[0],struct.unpack('<f',f.read(4))[0]]
            if (len(transformation[0])==4):
                vec.append(1)
            vec = linear_transformation.transform(transformation,vec)[:3] #Colon three jumpscare in case the user gave a matrix with 4 rows
            for v in vec:
                o.write(struct.pack('<f',v))
            vertices_read += 1
        if (chunk_length > data_length*12+2+6): raise Exception("VERTICES LIST has extra length!")
    else:
        o.write(f.read(chunk_length-6))
    read_chunk(f,o,size)
    
###Read the file
source_f.seek(0,2)
size = source_f.tell()
source_f.seek(0,0)
read_chunk(source_f,out_f,size)
        

source_f.close()
out_f.close()