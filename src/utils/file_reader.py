# read a file and return a matrix
def file_to_matrix(file_path : str):
    matrix = []
    file = open(file_path, "r")
    for line in file:
        row = [float(x) for x in line.split()]
        matrix.append(row)
    file.close()
    return matrix

def file_to_coor(file_path : str, size):
    matrix = []
    file = open(file_path, "r")
    for line in file:
        row = line.split()
        row[1] = float(row[1])
        row[2] = float(row[2])
        matrix.append(row)
    file.close()
    #if len(matrix)!= size: #Different size exception?
    #   
    return matrix
