#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import math
from pathlib import Path
from ttp_solvers import local_search, data

def solve_it(input_data):

    # parse the input
    points = data.read_data(input_data)

    # visit the nodes in the order they appear in the file
    solution, length, optimal = local_search.solve(np.array(points), Path("media"))

    return data.prepare_output(solution, length, optimal)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, "r") as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print(
            "This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)"
        )
