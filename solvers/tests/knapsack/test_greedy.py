import numpy as np
from numpy.testing import assert_array_equal

from my_solvers.knapsack.common import Item
from my_solvers.knapsack.greedy import Greedy


def test_init():
    greedy = Greedy()
    assert greedy.items is None
    assert greedy.capacity == 0


def test_assign():
    items = [Item(index, 1, 0) for index in range(10)]

    greedy = Greedy.from_input(10, items)
    value, optimal, solution = greedy.assign(items)
    assert value == 10
    assert optimal == 0
    assert_array_equal(solution, np.ones(len(items), dtype=int))


def test_solve():
    N_ITEMS = 10
    weights = np.random.choice(range(5), N_ITEMS)
    values = np.random.choice(range(5), N_ITEMS)

    items = [
        Item(index, values[index], weights[index]) for index in range(N_ITEMS)
    ]

    greedy = Greedy.from_input(10, items)
    value, optimal, solution = greedy.solve()

    assert value > 0
    assert optimal == 0
