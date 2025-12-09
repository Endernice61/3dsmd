def transform(matrix,vector):
    def apply(row,vec):
        component = 0
        for j,k in zip(row,vec):
            component += j*k
        return component
        
    out = []
    try:
        for i in matrix:
            out.append(apply(i,vector))
    except:
        raise Exception("Failed to apply the matrix to the vector")
    return out
