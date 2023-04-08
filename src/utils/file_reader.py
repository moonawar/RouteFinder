# read a file and return a matrix
def file_to_matrix(file_path : str):
    matrix = []
    file = open(file_path, "r")
    for line in file:
        row = [float(x) for x in line.split()]
        matrix.append(row)
    return matrix