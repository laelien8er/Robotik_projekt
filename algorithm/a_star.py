import math

class AStarAlgorithm:
    def __init__(self):
        self.grid = None
        self.end_node = None
        self.start_node = None
        self.heuristic = None
        self.list_open = []
        self.list_closed = []
        self.step_count = 0

    def find_path(self,
                  start_node: (int, int),
                  end_node: (int, int),
                  grid,
                  h: str = 'manhattan'):

        self.list_open.clear()
        self.list_closed.clear()

        self.heuristic = h
        self.start_node = start_node
        self.end_node = end_node
        self.grid = grid

        #  structure [(x,y), g, f, predecessor ]
        self.list_open.append([self.start_node, 0, 0, None])

        while self.list_open:
            self.list_open.sort(key=lambda x: x[2]) # sort by f
            best_node = self.list_open.pop(0)
            self.step_count += 1

            if best_node[0] == self.end_node:
                self.list_closed.append(best_node)
                return self.get_path()

            # Add best_node to closed list
            self.list_closed.append(best_node)

            for neighbor in self.neighbors(best_node):
                # continue if neighbor is in closed list
                if neighbor in [x[0] for x in self.list_closed]:
                    continue

                g_new = best_node[1] + 1

                open_positions = [x[0] for x in self.list_open]
                if neighbor in open_positions:
                    idx = open_positions.index(neighbor)
                    if g_new >= self.list_open[idx][1]:
                        continue
                    else:
                        self.list_open[idx][1] = g_new
                else:
                    pass

                # Calculate heuristic
                if self.heuristic == 'manhattan':
                    h = abs(self.end_node[0] - neighbor[0]) + abs(self.end_node[1] - neighbor[1])
                elif self.heuristic == 'euclidean':
                    h = math.sqrt((self.end_node[0] - neighbor[0]) ** 2 + (self.end_node[1] - neighbor[1]) ** 2)
                else:
                    # calculate manhatten distance if heuristic is unkown
                    print(f"Heuristic {h} is not defined; calculate manhattan-distance")
                    h = abs(self.end_node[0] - neighbor[0]) + abs(self.end_node[1] - neighbor[1])

                f = g_new + h

                if neighbor in open_positions:
                    idx = open_positions.index(neighbor)
                    self.list_open[idx][2] = f
                    self.list_open[idx][3] = best_node[0]
                else:
                    # Add to open list
                    self.list_open.append([neighbor, g_new, fl, best_node[0]])

        # no path was found
        return False

    def neighbors(self, node):
        row, column = node[0][0], node[0][1]
        nodes = []

        for j in [column - 1, column + 1]:
            if 0 <= j < len(self.grid[0]) and self.grid[row][j] == 0:
                nodes.append((row, j))

        for i in [row - 1, row + 1]:
            if 0 <= i < len(self.grid) and self.grid[i][column] == 0:
                nodes.append((i, column))

        return nodes

    def get_path(self):
        path = [self.end_node]
        current = self.list_closed[-1]

        while current[3] is not None:
            path.append(current[3])
            current_pos = current[3]
            idx = [x[0] for x in self.list_closed].index(current_pos)
            current = self.list_closed[idx]

        path.reverse()
        return path
