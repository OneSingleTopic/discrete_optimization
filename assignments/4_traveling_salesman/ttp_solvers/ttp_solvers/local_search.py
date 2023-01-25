import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from pathlib import Path
import shutil

from numpy.lib.stride_tricks import sliding_window_view

from scipy.spatial.distance import cdist

matplotlib.use("TkAgg")


def solve(points, n_iterations, media_folder=None):
    if media_folder:
        clean_folder(media_folder)

    distance_array = build_distance_matrix(points)
    n_iterations = 10

    initial_state = np.array(list(range(len(points))))
    solution, length = greedy(
        initial_state, two_opt, n_iterations, points, distance_array, media_folder
    )
    if media_folder is not None:
        display_tsp(
            points,
            solution,
            n_iterations + 1,
            media_folder=media_folder,
            color_str="g",
            name="solution",
        )
    return solution, 0


def clean_folder(media_folder):
    if media_folder.exists() and media_folder.is_dir():
        shutil.rmtree(media_folder)
    media_folder.mkdir()


def build_distance_matrix(points):
    return cdist(points, points)


def random_walk(state, distance_array=None, n_neighbors=1):
    return [np.random.permutation(state) for _ in range(n_neighbors)]


def n_opt(init_state: np.array, distance_array=None, n_opt=2):
    n_opt_neighbors = None

    sliding_windows = sliding_window_view(
        np.hstack([init_state, init_state[0], init_state[1]]), window_shape=3
    )

    for row_index, row in enumerate(sliding_windows):
        state, subpath = symetry_breaking(init_state), row
        for i in range(n_opt - 1):
            state, subpath = opt_state(state, distance_array, subpath)
            print(state)
            if n_opt_neighbors is None:
                n_opt_neighbors = state
            elif not (n_opt_neighbors == state).all(axis=1).any():
                n_opt_neighbors = np.vstack([n_opt_neighbors, state])

    return np.vstack(n_opt_neighbors)


def opt_state(state, distance_array, subpath):
    former_length = distance_array[subpath[1], subpath[2]]
    row_length = distance_array[subpath[1], :]
    min_index = np.argsort(row_length)[1]
    if min_index == subpath[2]:
        min_index = np.argsort(row_length)[2]

    start, end = (
        np.where(state == subpath[1])[0][0],
        np.where(state == min_index)[0][0],
    )
    flatten_state = state.flatten()
    ravel_state = np.hstack([flatten_state[start:], flatten_state[:start]])
    return_value = np.hstack([ravel_state[:end][::-1], ravel_state[end:]]).astype(int)

    return symetry_breaking(return_value), (
        return_value[-1],
        return_value[0],
        return_value[1],
    )


def symetry_breaking(solution):
    zero_index = np.argsort(solution)[0]
    next_index = zero_index + 1 if zero_index < (len(solution) - 1) else 0
    last_index = zero_index - 1

    if solution[next_index] < solution[last_index]:
        solution = solution[::-1]

    zero_index = np.argsort(solution)[0]

    return np.hstack([solution[zero_index:], solution[:zero_index]]).reshape(
        1, len(solution)
    )


def three_opt(state: np.array, distance_array=None, n_neighbors=None):
    two_opt_neighbors = np.zeros((state.shape[0], state.shape[0]))
    three_opt_neighbors = np.zeros((state.shape[0], state.shape[0]))

    sliding_windows = sliding_window_view(
        np.hstack([state, state[0], state[1]]), window_shape=3
    )
    for row_index, row in enumerate(sliding_windows):
        two_opt_neighbors[row_index, :], new_subpath = opt_state(
            state, distance_array, row
        )
        three_opt_neighbors[row_index, :], _ = opt_state(
            two_opt_neighbors[row_index, :], distance_array, new_subpath
        )

    return np.vstack([two_opt_neighbors, three_opt_neighbors])


def two_opt(state: np.array, distance_array=None, n_neighbors=None):
    neighbors = np.zeros((state.shape[0], state.shape[0]))
    sliding_windows = sliding_window_view(
        np.hstack([state, state[0], state[1]]), window_shape=3
    )
    for row_index, row in enumerate(sliding_windows):
        neighbors[row_index, :], _ = opt_state(state, distance_array, row)

    return neighbors


def greedy(state, get_neighbors, n_iterations, points, distance_array, media_folder):
    solution, length = state, compute_length(state, distance_array)
    for iteration in range(n_iterations):
        neighbors = get_neighbors(state, distance_array)
        neighbor = neighbors[0]
        if new_length := compute_length(neighbor, distance_array) < length:
            solution, length = state, new_length
    return solution, length


def compute_length(solution, distance_array):
    solution_temp = np.hstack([solution, solution[0]])
    return sum(
        distance_array[
            int(solution_temp[elem_index]), int(solution_temp[elem_index + 1])
        ]
        for elem_index, _ in enumerate(solution_temp[:-1])
    )


def display_tsp(
    points: list,
    solution: list,
    iteration: int,
    media_folder: Path,
    color_str: str = "b",
    name: str = "",
):
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.scatter(points[:, 0], points[:, 1])
    for index_point, point in enumerate(points):
        ax.annotate(
            index_point,
            (point[0], point[1]),
            fontsize=15,
            textcoords="offset points",
            xytext=(5, 10),
        )
    data_x, data_y = [], []
    for index_element, element in enumerate(solution):
        next_element = solution[0]
        if index_element < len(solution) - 1:
            next_element = solution[index_element + 1]
        data_x, data_y = points[element]
        delta_x, delta_y = (points[next_element] - points[element]) * 0.97
        ax.arrow(data_x, data_y, delta_x, delta_y, width=0.005, color=color_str)

    plt.savefig(media_folder / f"{iteration}_{name}.png")
    plt.close()
