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

def grid(data, row_labels, col_labels, ax=None, **kwargs):
    if ax is None:
        ax = plt.gca()

    # create custom colors
    # ToDo: schönere Farben aussuchen
    colors = ["#ffffcc", "#a1dab4", "#41b6c4", "#2c7fb8", "#253494"]
    custom_cmap = LinearSegmentedColormap.from_list("custom_cmap", colors)

    # Plot the heatmap
    im = ax.imshow(data, cmap=custom_cmap, **kwargs)

    # Show all ticks and label them with the respective list entries.
    ax.set_xticks(np.arange(len(data[0])), labels=col_labels)
    ax.set_yticks(np.arange(len(data[0])), labels=row_labels)

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=True, bottom=False,
                   labeltop=True, labelbottom=False)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=-30, ha="right",
             rotation_mode="anchor")

    # Turn spines off and create white grid.
    ax.spines[:].set_visible(False)

    ax.set_xticks(np.arange(len(data[0]) + 1) - .5, minor=True)
    ax.set_yticks(np.arange(len(data[0]) + 1) - .5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im


# ### Beispiel
#
# grid = [[0,0,0,0],
#         [0,0,0,0],
#         [1,0,0,1],
#         [0,0,0,0],
#        ]
#
# agent = (0,0)
# goal = (3,3)
#
# path = [(0,0), (0,1), (0,2), (1,2), (2,2), (3,2), (3,3)]
#
#
# data = get_grid_img(grid, agent, goal, path)
#
#
# fig, ax = plt.subplots()
#
# im = grid(data, range(len(data[0])), range(len(data[0])), ax=ax)
#
# fig.tight_layout()
# plt.show()
