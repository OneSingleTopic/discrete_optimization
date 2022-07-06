from collections import namedtuple

Item = namedtuple("Item", ["index", "value", "weight"])


class Solver(object):
    def __init__(self):
        self.capacity = 0
        self.items = None

    @classmethod
    def from_input(cls, capacity, items):
        dynamic_programing = cls()
        dynamic_programing.capacity = capacity
        dynamic_programing.items = items

        return dynamic_programing
