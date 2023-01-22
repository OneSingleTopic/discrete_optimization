import numpy as np 

def read_data(input_data):
    lines = input_data.split("\n")

    nodeCount = int(lines[0])
    points = np.zeros((nodeCount, 2))
    for i in range(1, nodeCount + 1):
        line = lines[i]
        parts = line.split()
        points[i-1, :] = np.array([float(parts[0]), float(parts[1])])

    return points

def prepare_output(solution, length, optimal):
    # prepare the solution in the specified output format
    output_data = "%.2f" % length + " " + str(optimal) + "\n"
    output_data += " ".join(map(str, solution))

    return output_data
