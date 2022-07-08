from ortools.sat.python import cp_model
from pprint import pprint
from dataclasses import dataclass


def solve(fire_stations, items_count):

    model = cp_model.CpModel()

    # VARIABLES
    variables = [
        model.NewBoolVar(str(fire_station.index))
        for fire_station in fire_stations
    ]

    # CONSTRAINTS
    for item in range(items_count):
        concerned_stations = [
            fire_station
            for fire_station in fire_stations
            if item in fire_station.items
        ]
        model.Add(
            sum(
                variables[fire_station.index]
                for fire_station in concerned_stations
            )
            >= 1
        )

    # OBJECTIVE
    cost = sum(
        variable * fire_stations[index].cost
        for index, variable in enumerate(variables)
    )
    model.Minimize(cost)

    # SOLVER
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 10.0
    status = solver.Solve(model)

    if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
        solution = [solver.Value(variable) for variable in variables]
    else:
        raise ValueError("CP solver has not converge")

    return solution, int(status == cp_model.OPTIMAL)
