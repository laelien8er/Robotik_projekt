import json
import math


class AStarAlgorithm:
    def __init__(
            self,
            start_node: (int, int),
            end_node: (int, int),
            grid,
            h: str = 'manhattan'):

        self.heuristic = h
        self.start_node = start_node
        self.end_node = end_node
        self.grid = grid
        self.list_open = []
        self.list_closed = []

    def find_path(self):
        self.list_open.append([self.start_node, 0, 0, (0, 0)])  # node with ((x,y),g, f=g+h,(predecessor x,y))

        while True:
            self.list_open.sort(key=lambda x: x[2])
            best_node = self.list_open.pop(0)

            if best_node[0] == self.end_node:
                print('path_found')
                self.list_closed.append(best_node)
                return self.get_path()
            self.list_closed.append(best_node)

            for neighbor in self.neighbors(best_node):
                if neighbor in self.list_closed[0]: continue

                g_new = best_node[1] + 1  # in the grid all the steps have the same weight

                if self.list_open and neighbor in [x[0] for x in self.list_open]:
                    if g_new >= self.list_open[[x[0] for x in self.list_open].index(neighbor)][1]:
                        continue
                    else:
                        self.list_open[self.list_open[0].index(neighbor)][1] = g_new

                if self.heuristic == 'manhattan':
                    h = abs(self.end_node[0] - neighbor[0]) + abs(self.end_node[1] - neighbor[1])

                elif self.heuristic == 'airplane':
                    h = math.sqrt(pow((self.end_node[0] - neighbor[0]), 2) + pow((self.end_node[1] - neighbor[1]), 2))

                if self.list_open and neighbor in [x[0] for x in self.list_open]:
                    # update f if node already exists
                    self.list_open[self.list_open[0].index(neighbor)][2] = g_new+h
                else:
                    self.list_open.append([neighbor, g_new, g_new+h, best_node[0]])
            if len(self.list_open) == 0:
                break
        return 'no path could be found'

    def neighbors(self, node):
        row = node[0][0]
        column = node[0][1]
        nodes = []
        for j in [column - 1, column + 1]:
            if len(self.grid[0]) > j >= 1 != self.grid[row][j]:
                nodes.append((row, j))
        for i in [row - 1, row + 1]:
            if len(self.grid) > i >= 1 != self.grid[i][column]:
                nodes.append((i, column))
        return nodes

    def get_path(self):
        node = self.list_closed[-1]
        path = [(self.end_node)]
        while True:
            path.append(node[3])
            if node[3] == self.start_node:
                return path
            node = self.list_closed[[x[0] for x in self.list_closed].index(node[3])]


# file_path = "/home/lea/Dokumente/WS24_25/Robotik_projekt/simulation/grid_test.json"
# with open(file_path, 'r') as file:
#     map_data = json.load(file)
#
# start = (map_data['agent_x'], map_data['agent_y'])
# end = (map_data['goal_x'], map_data['goal_y'])
# grid = map_data['grid']
#
# p = AStarAlgorithm(start, end, grid, h='airplane').find_path()
# print(p)