import os

from my_solvers.knapsack import knapsack

RESOURCES_FOLDER = "resources/knapsack/data"
SIMPLE_DATA = os.path.join(RESOURCES_FOLDER, "simple")


def test_parse_input():
    with open(SIMPLE_DATA, "r") as input_data_file:
        input_data = input_data_file.read()
        item_count, capacity, items = knapsack.parse_input(input_data)
        assert item_count == 4
        assert capacity == 11
        assert item_count == len(items)
