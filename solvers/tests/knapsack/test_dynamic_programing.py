import numpy as np
from numpy.testing import assert_array_equal

from my_solvers.knapsack.common import Item
from my_solvers.knapsack.dynamic_programing import Dynamic_Programing


def test_init():
    dynamic_programing = Dynamic_Programing()

    assert dynamic_programing is not None
    assert dynamic_programing.capacity == 0
    assert dynamic_programing.items is None

    dynamic_programing = Dynamic_Programing.from_input(10, [])

    assert dynamic_programing is not None
    assert dynamic_programing.capacity == 10
    assert dynamic_programing.items == []


def test_table():
    dynamic_programing = Dynamic_Programing.from_input(
        10, [Item(0, 2, 3), Item(1, 2, 3)]
    )

    assert dynamic_programing is not None

    assert_array_equal(dynamic_programing.table.shape, (11, 3))
    objective, optimal, solution = dynamic_programing.solution
    assert objective == 4
    assert optimal == 1
    assert_array_equal(solution, np.array([1, 1]))
