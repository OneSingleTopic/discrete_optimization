import numpy as np

from .common import Solver, Item


class Greedy(Solver):
    def solve(self):
        sorted_items = self.sort_items()
        return self.assign(sorted_items)

    def sort_items(self):
        return sorted(self.items, key=lambda x: x.value / max(1, x.weight))

    def assign(self, items):
        weight = 0
        value = 0
        solution = np.zeros(len(self.items), dtype=int)

        for item in items:
            if item.weight + weight <= self.capacity:
                value += item.value
                weight += item.weight
                solution[item.index] += 1

        return value, 0, solution
