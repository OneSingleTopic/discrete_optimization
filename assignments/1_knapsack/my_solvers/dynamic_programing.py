import numpy as np

from .common import Solver, Item


class Dynamic_Programing(Solver):
    def __init__(self):
        super().__init__()
        self.table = None

    @classmethod
    def from_input(cls, capacity, items):
        if len(items) > 100:
            LIM_CAPACITY, LIM_ITEMS = 100_000, 1_000
        else:
            LIM_CAPACITY, LIM_ITEMS = capacity, len(items)

        print("LIMITS ITEMS", len(items), LIM_ITEMS)
        print("LIMITS CAPACITY", capacity, LIM_CAPACITY)

        dynamic_programing = cls()
        dynamic_programing.capacity_full = capacity
        dynamic_programing.capacity = min(capacity, LIM_CAPACITY)
        dynamic_programing.items_full = items
        dynamic_programing.items = items[: min(len(items), LIM_ITEMS)]

        dynamic_programing.table = dynamic_programing.build_table()

        return dynamic_programing

    @property
    def solution(self):
        X, Y = self.table.shape
        X, Y = X - 1, Y - 1
        objective = self.table[X, Y]
        solution = np.zeros(len(self.items_full))
        while Y > 0:
            item_index = Y - 1
            if self.is_in_solution(X, Y):
                solution[item_index] = 1
                X -= self.items[item_index].weight
            Y -= 1
        return (
            int(objective),
            self.is_optimal,
            solution.astype(int),
        )

    @property
    def is_optimal(self):
        print("ITEMS", len(self.items), len(self.items_full))
        print("CAPACITY", self.capacity, self.capacity_full)

        return int(
            (len(self.items) == len(self.items_full))
            & (self.capacity == self.capacity_full)
        )

    def is_in_solution(self, X, Y):
        if self.table[X, Y - 1] == self.table[X, Y]:
            return False
        else:
            return True

    def build_table(self):
        table = np.zeros((self.capacity + 1, len(self.items) + 1), dtype=int)
        for item in self.items:
            item_index = item.index + 1
            for slot in range(self.capacity + 1):
                table[slot, item_index] = self.grand_o(slot, item, table)

        return table

    def grand_o(self, slot, item, table):
        item_index = item.index + 1
        if item.weight > slot:
            return int(table[slot, item_index - 1])
        else:
            return int(
                max(
                    table[slot - item.weight, item_index - 1] + item.value,
                    table[slot, item_index - 1],
                )
            )
