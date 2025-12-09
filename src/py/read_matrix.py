import sys

def read_matrix():
    out = []
    try:
        inputmatrix = sys.argv[2]
    except:
        print('Please enter a matrix in the form "1, 0, 0 \\\\ 0, 1, 0 \\\\ 0, 0, 1"\nIf a fourth column is specified, it will be used as a translation')
        inputmatrix = input()
    try:
        rows = inputmatrix.rsplit("\\")
        if(inputmatrix.count("\\\\") > 0): rows = inputmatrix.rsplit("\\\\")
        for i in rows:
            row = []
            for j in i.rsplit(","):
                row.append(float(j))
            out.append(row)
    except:
        raise Exception("Matrix input error")
    return out
