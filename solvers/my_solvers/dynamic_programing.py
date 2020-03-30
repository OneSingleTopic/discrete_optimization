import numpy as np


class Dynamic_Programing(object):
    def __init__(self):
        self.capacity = 0
        self.reward = 0
        self.items = None
        self.assignment = None
        self.table = None

    @classmethod
    def from_input(cls, capacity, items):
        dynamic_programing = cls()
        dynamic_programing.capacity = capacity
        dynamic_programing.items = items
        dynamic_programing.assignment = [0 for _ in items]
        dynamic_programing.table = dynamic_programing.build_table()

        return dynamic_programing

    def get_solution(self):
        pass

    def build_table(self):
        table = np.zeros((self.capacity, len(self.items)))

        return table
