import sys
import smd
import linear_transformation
import write

class _3ds:
    def __init__(self,name="Selection"):
        self.object_name = name+"\0"
        self.vertices = []
        self.polygons = []

###Read file name
try:
    source_file_input_string = sys.argv[1]
except:
    print("Please enter the file you would like to transform: ")
    source_file_input_string = input()

###Open input file
try:
    source_f = open(source_file_input_string)
except:
    print("File failed to open")
    exit()

###Open output file + input file type check
try:
    output_file_input_string = source_file_input_string.replace(".smd",".3ds")
    if (output_file_input_string == source_file_input_string): raise Exception()
    output_file = open(output_file_input_string,"wb")
except:
    print("The file is not an .smd")
    source_f.close()
    exit()

scale = 1/128

###Transformation matrix. Might be dependant on handle, but Konclan assures me it makes no difference
transformation = [[0,0,-scale],[scale,0,0],[0,scale,0]]

###Function definition
def discard_to(input_f,stop_string):
    line = input_f.readline()
    while (line != '' and line != stop_string):
        line = input_f.readline()
    return

##Read to end of animation
discard_to(source_f,'triangles\n')

model = _3ds(name="Selection")

###Read vertices and triangles
line = source_f.readline() #Texture
while (line != '' and line != 'end\n'):
    model.polygons.append([])
    v = linear_transformation.transform(transformation,smd.read_vertex(source_f))
    if v not in model.vertices: model.vertices.append(v)
    model.polygons[-1].append(model.vertices.index(v))
    v = linear_transformation.transform(transformation,smd.read_vertex(source_f))
    if v not in model.vertices: model.vertices.append(v)
    model.polygons[-1].append(model.vertices.index(v))
    v = linear_transformation.transform(transformation,smd.read_vertex(source_f))
    if v not in model.vertices: model.vertices.append(v)
    model.polygons[-1].append(model.vertices.index(v))
    line = source_f.readline() #Texture
write.write(model,output_file)

source_f.close()
output_file.close()
