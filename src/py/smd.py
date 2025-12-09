def read_vertex(input_f):
    return parse_vertex(input_f.readline())

def parse_vertex(input_string):
    data = input_string.rsplit()
    return [float(data[1]),float(data[2]),float(data[3])]
