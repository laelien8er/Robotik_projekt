from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import matplotlib.pyplot as plt


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


### Beispiel

# data = get_grid_img(grid, agent, goal, path)
#
# fig, ax = plt.subplots()
# im = get_grid(data,  ax=ax)
# fig.tight_layout()
# plt.axis('off')
# plt.show()
