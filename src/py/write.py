import struct
def write(_3ds,out_f):
    polygons_number = len(_3ds.polygons)
    faces_description_len = polygons_number*8+2+6
    vertices_number = len(_3ds.vertices)
    vertices_list_len = vertices_number*12+2+6
    triangular_mesh_len = faces_description_len+vertices_list_len+6
    object_block_len = len(_3ds.object_name)+triangular_mesh_len+6
    _3d_editor_chunk_len = object_block_len+6
    main_chunk_len = _3d_editor_chunk_len+6
    out_f.write(b'\x4d\x4d')
    out_f.write(int.to_bytes(main_chunk_len,length=4,byteorder='little'))
    out_f.write(b'\x3d\x3d')
    out_f.write(int.to_bytes(_3d_editor_chunk_len,length=4,byteorder='little'))
    out_f.write(b'\x00\x40')
    out_f.write(int.to_bytes(object_block_len,length=4,byteorder='little'))
    out_f.write(_3ds.object_name.encode("utf-8"))
    out_f.write(b'\x00\x41')
    out_f.write(int.to_bytes(triangular_mesh_len,length=4,byteorder='little'))
    out_f.write(b'\x10\x41')
    out_f.write(int.to_bytes(vertices_list_len,length=4,byteorder='little'))
    out_f.write(int.to_bytes(vertices_number,length=2,byteorder='little'))
    for v in _3ds.vertices:
        for f in v:
            out_f.write(struct.pack('<f',f))
    out_f.write(b'\x20\x41')
    out_f.write(int.to_bytes(faces_description_len,length=4,byteorder='little'))
    out_f.write(int.to_bytes(polygons_number,length=2,byteorder='little'))
    for p in _3ds.polygons:
        for v in p:
            out_f.write(int.to_bytes(v,length=2,byteorder='little'))
        out_f.write(b'\x00\x00')
