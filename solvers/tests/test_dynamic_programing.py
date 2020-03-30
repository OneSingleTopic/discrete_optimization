import numpy as np
from numpy.testing import assert_array_equal
from my_solvers.dynamic_programing import Dynamic_Programing


def test_init():
    dynamic_programing = Dynamic_Programing()

    assert dynamic_programing is not None
    assert dynamic_programing.capacity == 0
    assert dynamic_programing.reward == 0
    assert dynamic_programing.items is None
    assert dynamic_programing.assignment is None

    dynamic_programing = Dynamic_Programing.from_input(10, [])

    assert dynamic_programing is not None
    assert dynamic_programing.capacity == 10
    assert dynamic_programing.reward == 0
    assert dynamic_programing.items == []
    assert dynamic_programing.assignment == []


def test_table():
    dynamic_programing = Dynamic_Programing.from_input(10, [1, 2])

    assert dynamic_programing is not None
    assert_array_equal(dynamic_programing.table, np.zeros((10, 2)))
