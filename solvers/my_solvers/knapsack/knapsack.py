from collections import namedtuple

from my_solvers.knapsack.common import Item
from my_solvers.knapsack.greedy import Greedy
from my_solvers.knapsack.dynamic_programing import Dynamic_Programing


def parse_input(input_data):
    lines = input_data.split("\n")

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count + 1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i - 1, int(parts[0]), int(parts[1])))

    return item_count, capacity, items


def solve(capacity, items):

    # if len(items) > 100:
    #     return Greedy.from_input(capacity, items).solve()

    return Dynamic_Programing.from_input(capacity, items).solution
