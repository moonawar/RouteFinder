# read a file and return the 
#     adjacency matrix
#     node names (if specified)
#     node coordinates (if specified)

def read_file_to_nodes(file_path : str):
    nodes = []
    node_names = []
    nodes_coordinates = []
    file = open(file_path, "r")
    line = file.readline()
    row = [float(x) for x in line.split()]
    nodes.append(row)

    matrix_size = len(row)

    for _ in range(matrix_size - 1):
        line = file.readline()
        row = [float(x) for x in line.split()]
        nodes.append(row)
    
    try:
        line = file.readline()
    except:
        return nodes, None, None
    
    try:
        row = line.split()
        row_len = len(row)
        node_name = ""
        for i in range(0, row_len - 2):
            node_name += row[i]
            node_name += " " if i != row_len - 3 else ""

        node_names.append(node_name)
        nodes_coordinates.append([float(row[-2]), float(row[-1])])
    except:
        return None, None, None
    
    for _ in range(matrix_size - 1):
        try:
            line = file.readline()
            row = line.split()
            row_len = len(row)
            node_name = ""
            for i in range(0, row_len - 2):
                node_name += row[i]
                node_name += " " if i != row_len - 3 else ""

            node_names.append(node_name)
            nodes_coordinates.append([float(row[-2]), float(row[-1])])
        except:
            return None, None, None
    
    return nodes, node_names, nodes_coordinates
