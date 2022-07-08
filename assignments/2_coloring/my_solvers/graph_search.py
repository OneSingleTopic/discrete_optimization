def solve(node_count, edges):
    solution = [None for _ in range(node_count)]

    edges_adjacents = [
        (
            node,
            [
                elem[0] if elem[0] != node else elem[1]
                for elem in list(
                    filter(lambda x: (x[0] == node or x[1] == node), edges)
                )
            ],
        )
        for node in range(node_count)
    ]
    colors = [0]
    while any(s is None for s in solution):
        first_node = max(
            [elem for elem in edges_adjacents if solution[elem[0]] is None],
            key=lambda item: len(item[1]),
        )[0]
        to_visit = [first_node]

        while to_visit:
            current_elem = to_visit.pop(0)
            neighbors = edges_adjacents[current_elem][1]
            for color in colors:
                if all(
                    solution[neighbor] is None or solution[neighbor] != color
                    for neighbor in neighbors
                ):
                    solution[current_elem] = color
                    break
            if solution[current_elem] is None:
                solution[current_elem] = len(colors)
                colors.append(len(colors))

            for neighbor in neighbors:
                if solution[neighbor] is None:
                    to_visit.append(neighbor)

    return colors, solution, 0
