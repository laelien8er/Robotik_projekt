# import math
#
# class AStarAlgorithm:
#     def __init__(self):
#         self.heuristic = None
#         self.start_node = None
#         self.end_node = None
#         self.grid = None
#         self.list_open = []
#         self.list_closed = []
#
#     def find_path(self,
#             start_node: (int, int),
#             end_node: (int, int),
#             grid,
#             h: str = 'manhattan'):
#
#         # Reset lists for each run
#         self.list_open.clear()
#         self.list_closed.clear()
#
#         self.heuristic = h
#         self.start_node = start_node
#         self.end_node = end_node
#         self.grid = grid
#         self.list_open.append([self.start_node, 0, 0, (0, 0)])  # node with ((x,y),g, f=g+h,(predecessor x,y))
#
#         while True:
#             self.list_open.sort(key=lambda x: x[1])
#             best_node = self.list_open.pop(0)
#
#             if best_node[0] == self.end_node:
#                 print('path_found')
#                 self.list_closed.append(best_node)
#                 return self.get_path()
#             self.list_closed.append(best_node)
#
#             for neighbor in self.neighbors(best_node):
#                 if neighbor in self.list_closed[0]: continue
#
#                 g_new = best_node[1] + 1  # in the grid all the steps have the same weight
#
#                 if self.list_open and neighbor in [x[0] for x in self.list_open]:
#                     if g_new >= self.list_open[[x[0] for x in self.list_open].index(neighbor)][1]:
#                         continue
#                     else:
#                         self.list_open[self.list_open[0].index(neighbor)][1] = g_new
#
#                 if self.heuristic == 'manhattan':
#                     h = abs(self.end_node[0] - neighbor[0]) + abs(self.end_node[1] - neighbor[1])
#
#                 elif self.heuristic == 'euclidean':
#                     h = math.sqrt(pow((self.end_node[0] - neighbor[0]), 2) + pow((self.end_node[1] - neighbor[1]), 2))
#
#                 if self.list_open and neighbor in [x[0] for x in self.list_open]:
#                     # update f if node already exists
#                     self.list_open[self.list_open[0].index(neighbor)][2] = g_new+h
#                 else:
#                     self.list_open.append([neighbor, g_new, g_new+h, best_node[0]])
#             if len(self.list_open) == 0:
#                 break
#         return False
#
#     def neighbors(self, node):
#         row = node[0][0]
#         column = node[0][1]
#         nodes = []
#         for j in [column - 1, column + 1]:
#             if len(self.grid[0]) > j >= 1 != self.grid[row][j]:
#                 nodes.append((row, j))
#         for i in [row - 1, row + 1]:
#             if len(self.grid) > i >= 1 != self.grid[i][column]:
#                 nodes.append((i, column))
#         return nodes
#
#     def get_path(self):
#         node = self.list_closed[-1]
#         path = [(self.end_node)]
#         while True:
#             path.append(node[3])
#             if node[3] == self.start_node:
#                 return path
#             node = self.list_closed[[x[0] for x in self.list_closed].index(node[3])]


import math

class AStarAlgorithm:
    def __init__(self):
        self.grid = None
        self.end_node = None
        self.start_node = None
        self.heuristic = None
        self.list_open = []
        self.list_closed = []

    def find_path(self,
                  start_node: (int, int),
                  end_node: (int, int),
                  grid,
                  h: str = 'manhattan'):
        # Reset lists for each run
        self.list_open.clear()
        self.list_closed.clear()

        self.heuristic = h
        self.start_node = start_node
        self.end_node = end_node
        self.grid = grid

        # Append start node: structure [ (x,y), g, f, predecessor ]
        # Predecessor of start node can be None
        self.list_open.append([self.start_node, 0, 0, None])

        while self.list_open:
            # Sort by f-cost (index 2)
            self.list_open.sort(key=lambda x: x[2])
            best_node = self.list_open.pop(0)

            # If we reached the goal
            if best_node[0] == self.end_node:
                self.list_closed.append(best_node)
                # print('path_found')
                return self.get_path()

            # Add best_node to closed list
            self.list_closed.append(best_node)

            for neighbor in self.neighbors(best_node):
                # If neighbor is already in closed list, skip
                if neighbor in [x[0] for x in self.list_closed]:
                    continue

                g_new = best_node[1] + 1  # assume uniform cost

                open_positions = [x[0] for x in self.list_open]
                if neighbor in open_positions:
                    # Check if we found a better path (lower g)
                    idx = open_positions.index(neighbor)
                    if g_new >= self.list_open[idx][1]:
                        # Not a better path
                        continue
                    else:
                        # Better path found, update g, and also update f
                        self.list_open[idx][1] = g_new
                else:
                    # Not in open list, we need to calculate h and add it
                    pass

                # Calculate heuristic
                if self.heuristic == 'manhattan':
                    h_val = abs(self.end_node[0] - neighbor[0]) + abs(self.end_node[1] - neighbor[1])
                elif self.heuristic == 'euclidean':
                    h_val = math.sqrt((self.end_node[0] - neighbor[0]) ** 2 + (self.end_node[1] - neighbor[1]) ** 2)
                else:
                    # Default to manhattan if unknown heuristic
                    h_val = abs(self.end_node[0] - neighbor[0]) + abs(self.end_node[1] - neighbor[1])

                f_val = g_new + h_val

                if neighbor in open_positions:
                    # Update f in the open list
                    idx = open_positions.index(neighbor)
                    self.list_open[idx][2] = f_val
                    self.list_open[idx][3] = best_node[0]
                else:
                    # Add to open list
                    self.list_open.append([neighbor, g_new, f_val, best_node[0]])

        # no path was found
        return False

    def neighbors(self, node):
        # node: [ (x,y), g, f, pred ]
        row, column = node[0][0], node[0][1]
        nodes = []

        # Check left and right
        for j in [column - 1, column + 1]:
            if 0 <= j < len(self.grid[0]) and self.grid[row][j] == 0:
                nodes.append((row, j))

        # Check up and down
        for i in [row - 1, row + 1]:
            if 0 <= i < len(self.grid) and self.grid[i][column] == 0:
                nodes.append((i, column))

        return nodes

    def get_path(self):
        # Reconstruct path by following predecessors backward
        path = [self.end_node]
        current = self.list_closed[-1]

        while current[3] is not None:  # until we reach the start (which has predecessor None)
            path.append(current[3])
            current_pos = current[3]
            # find predecessor node in closed list
            idx = [x[0] for x in self.list_closed].index(current_pos)
            current = self.list_closed[idx]

        # Reverse path to start->end order
        path.reverse()
        return path
