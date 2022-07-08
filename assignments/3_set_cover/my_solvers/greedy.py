def solve(sets, item_count):
    solution = [0 for _ in sets]
    coverted = set()

    for s in sets:
        solution[s.index] = 1
        coverted |= set(s.items)
        if len(coverted) >= item_count:
            break

    return solution, 0
