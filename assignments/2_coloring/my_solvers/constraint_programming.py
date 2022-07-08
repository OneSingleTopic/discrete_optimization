from ortools.sat.python import cp_model
from pprint import pprint
from dataclasses import dataclass


@dataclass
class Node:
    id: int
    neighbors: list

    def __repr__(self):
        return str(self.id)


def solve(node_count, edges):
    model = cp_model.CpModel()
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

    nodes = [Node(node_id, []) for node_id, _ in edges_adjacents]

    for node_id, neighbors in edges_adjacents:
        nodes[node_id].neighbors = [nodes[neighbor] for neighbor in neighbors]

    variables = [
        model.NewIntVar(0, node_count, str(node_id))
        for node_id, neighbors in edges_adjacents
    ]
    maximum_color_number = model.NewIntVar(
        0,
        node_count,
        "max_number_color",
    )

    for variable in variables:
        model.Add(variable <= maximum_color_number)

    print(node_count)
    solver = cp_model.CpSolver()

    # FINDING CLIQUES IS EXPENSIVE
    if node_count <= 200:
        cliques = []
        cliques = find_cliques_simple(edges_adjacents)
        # find_cliques(remaining_nodes=nodes, cliques=cliques)
        print("FOUND_CLIQUES")
        clic_constraints(model, variables, cliques)
        solver.parameters.max_time_in_seconds = 20.0
    else:
        solver.parameters.max_time_in_seconds = 300.0

    for edge in edges:
        model.Add(variables[edge[0]] != variables[edge[1]])

    model.Minimize(maximum_color_number)

    status = solver.Solve(model)

    if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
        solution = [solver.Value(variable) for variable in variables]
    else:
        raise ValueError("CP solver has not converge")

    return (
        list(set(solution)),
        solution,
        cp_model.OPTIMAL == status,
    )


def clic_constraints(model, variables, cliques):
    for clique in cliques:
        model.AddAllDifferent(
            [variables[element_clique] for element_clique in clique]
        )

    biggest_clic = sorted(cliques, key=lambda clic: len(clic), reverse=True)[0]
    for index, element in enumerate(biggest_clic):
        model.Add(variables[element] == index)


def find_cliques_simple(edges_adjacents):
    global_clics = []
    for node_id, neighbors in edges_adjacents:
        for neighbor in neighbors:
            new_clic = {node_id, neighbor}
            _, neighbors_1 = edges_adjacents[neighbor]
            for clic_candidate in neighbors_1:
                _, neighbors_2 = edges_adjacents[clic_candidate]
                if all(
                    (element in neighbors_2) or (element == neighbor)
                    for element in new_clic
                ):
                    new_clic.add(clic_candidate)
            if not new_clic in global_clics:
                global_clics.append(new_clic)

    return global_clics


def find_cliques(
    potential_clique=[], remaining_nodes=[], skip_nodes=[], cliques=[], depth=0
):
    if len(remaining_nodes) == 0 and len(skip_nodes) == 0:
        cliques.append(potential_clique)
        return 1

    found_cliques = 0
    for node in remaining_nodes:
        # Try adding the node to the current potential_clique to see if we can make it work.
        new_potential_clique = potential_clique + [node]
        new_remaining_nodes = [
            n for n in remaining_nodes if n in node.neighbors
        ]
        new_skip_list = [n for n in skip_nodes if n in node.neighbors]
        found_cliques += find_cliques(
            new_potential_clique,
            new_remaining_nodes,
            new_skip_list,
            cliques,
            depth + 1,
        )

        # We're done considering this node.  If there was a way to form a clique with it, we
        # already discovered its maximal clique in the recursive call above.  So, go ahead
        # and remove it from the list of remaining nodes and add it to the skip list.
        remaining_nodes.remove(node)
        skip_nodes.append(node)
    return found_cliques
