import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from pathlib import Path
import shutil


from scipy.spatial.distance import cdist

matplotlib.use("TkAgg")


def solve(points, media_folder):
    clean_folder(media_folder)
    distance_array = build_distance_matrix(points)
    length = np.inf
    for iteration in range(10):
        new_solution = np.random.permutation(range(0, len(points)))
        if (
            new_length := compute_length(new_solution, distance_array)
        ) < length:
            solution, length = new_solution, new_length
            display_tsp(points, solution, iteration, media_folder=media_folder)
        else:
            display_tsp(
                points,
                new_solution,
                iteration,
                media_folder=media_folder,
                color_str="r",
                name="worst",
            )

    display_tsp(
        points,
        solution,
        iteration + 1,
        media_folder=media_folder,
        color_str="g",
        name="solution",
    )
    return solution, 0


def compute_length(solution, distance_array):
    return (
        sum(
            distance_array[solution[elem_index - 1], elem]
            for elem_index, elem in enumerate(solution)
        )
        + distance_array[solution[-1], 0]
    )


def build_distance_matrix(points):
    return cdist(points, points)


def clean_folder(media_folder):
    if media_folder.exists() and media_folder.is_dir():
        shutil.rmtree(media_folder)
    media_folder.mkdir()


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
            fontsize=12,
            textcoords="offset points",
            xytext=(0, 10),
        )
    data_x, data_y = [], []
    for index_element, element in enumerate(solution):
        next_element = solution[0]
        if index_element < len(solution) - 1:
            next_element = solution[index_element + 1]
        data_x, data_y = points[element]
        delta_x, delta_y = (points[next_element] - points[element]) * 0.97
        ax.arrow(data_x, data_y, delta_x, delta_y, width=10, color=color_str)

    plt.savefig(media_folder / f"{iteration}_{name}.png")
    plt.close()
