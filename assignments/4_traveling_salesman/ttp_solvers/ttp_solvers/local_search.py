import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from pathlib import Path
import shutil

from scipy.spatial.distance import cdist

matplotlib.use("TkAgg")

def solve(points, n_iterations, media_folder=None):
    if media_folder : clean_folder(media_folder)

    distance_array = build_distance_matrix(points)
    n_iterations = 10

    initial_state = list(range(len(points)))
    solution, length = greedy(
        initial_state,
        random_walk,
        n_iterations, 
        points, 
        distance_array,
        media_folder
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

def random_walk(state, n_neighbors=1):
    return [np.random.permutation(state) for _ in range(n_neighbors)]

def greedy(
    state, 
    get_neighbors,
    n_iterations, 
    points, 
    distance_array, 
    media_folder):
    solution, length = state, compute_length(state, distance_array)
    for iteration in range(n_iterations):
        neighbors = get_neighbors(state)
        neighbor = neighbors[0]
        if (new_length := compute_length(neighbor, distance_array) < length):
            solution, length = state, new_length
    return solution, length


def compute_length(solution, distance_array):
    return (
        sum(
            distance_array[solution[elem_index], elem]
            for elem_index, elem in enumerate(solution)
        )
        + distance_array[solution[-1], solution[0]]
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




