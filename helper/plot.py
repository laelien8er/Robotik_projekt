from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import matplotlib.pyplot as plt
from simulation import CreateGrid
from algorithm import AStarAlgorithm, WavefrontAlgorithm, MeetInTheMiddleAlgorithm


def get_grid_img(grid, agent, goal, path=False):
    data = grid
    if path:
        for p in path:
            data[p[0]][p[1]] = 4

    data[agent[0]][agent[1]] = 2
    data[goal[0]][goal[1]] = 3
    return data

def get_grid(data, ax=None, **kwargs):
    if ax is None:
        ax = plt.gca()

    # create custom colors
    colors = ["#F1E2D2", "#DCCCA5", "#BCA2AA", "#C6858D", "#D5B2B2"]
    custom_cmap = LinearSegmentedColormap.from_list("custom_cmap", colors)

    # Plot the heatmap
    im = ax.imshow(data, cmap=custom_cmap, **kwargs)

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=True, bottom=False,
                   labeltop=True, labelbottom=False)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=-90, ha="right",
             rotation_mode="anchor")

    return im

def create_show_grid(algorithm: str = False, grid: str = 'detour_grid', size_grid: int = 32):

    if algorithm == 'A-star':
        alg = AStarAlgorithm()
    elif algorithm == 'Wavefront':
        alg = WavefrontAlgorithm()
    elif algorithm == 'MITM':
        alg = MeetInTheMiddleAlgorithm()
    else:
        print(f"Algorithm {algorithm} not found")
        return False

    grid_creator = CreateGrid()
    grid_dict = grid_creator.create_grid(grid, size_grid)

    start = (grid_dict['agent_x'], grid_dict['agent_y'])
    end = (grid_dict['goal_x'], grid_dict['goal_y'])
    grid = grid_dict['grid']


    path, _ = alg.find_path(start, end, grid)

    data = get_grid_img(grid, start, end, path)

    return data

def get_actions(path, start):
    # check if path is start to end
    if path[0] != start:
        path.reverse()

    actions = []
    p_last = path[0]
    for p in path[1:]:
        if p[1] == p_last[1]:
            if p[0] < p_last[0]:
                actions.append(1)  # step up
            elif p[0] > p_last[0]:
                actions.append(3)  # step down
        elif p[0] == p_last[0]:
            if p[1] > p_last[1]:
                actions.append(0)  # step right
            elif p[1] < p_last[1]:
                actions.append(2)  # step left
        p_last = p
    return actions


