from collections import deque


class WavefrontAlgorithm:
    def __init__(self, grid, start, goal):
        self.grid = grid
        self.start = start
        self.goal = goal
        self.rows = len(grid)
        self.cols = len(grid[0])

        # init distanz und parent
        self.distance = [[float('inf')] * self.cols for _ in range(self.rows)]
        self.parent = [[None] * self.cols for _ in range(self.rows)]

        # start- und zielkoordinaten
        (self.agent_x, self.agent_y) = self.start
        (self.goal_x, self.goal_y) = self.goal

        # prüfen, ob start oder ziel blockiert
        if self.grid[self.agent_x][self.agent_y] or self.grid[self.goal_x][self.goal_y]:
            raise ValueError("Start oder Ziel ist blockiert.")

    def wavefront(self):
        # distanz des starts auf 0 setzen
        self.distance[self.agent_x][self.agent_y] = 0

        # queue für bfs, startknoten einfügen
        queue = deque([self.start])

        # bfs wavefront ausführen
        while queue:
            x, y = queue.popleft()

            # wenn goal erreicht, abbruch
            if (x, y) == (self.goal_x, self.goal_y):
                break

            # für alle nachbarn prüfen, in 4 richtungen
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                # prüfen, ob nachbar innerhalb des grids und frei (inf)
                if 0 <= nx < self.rows and 0 <= ny < self.cols:
                    if not self.grid[nx][ny] and self.distance[nx][ny] == float('inf'):
                        self.distance[nx][ny] = self.distance[x][y] + 1
                        self.parent[nx][ny] = (x, y)
                        queue.append((nx, ny))

        # wenn goal nicht erreichbar
        if self.distance[self.goal_x][self.goal_y] == float('inf'):
            raise ValueError("Kein Pfad gefunden.")

        # distanz und parent zurückgeben, um außerhalb pfad zu rekonstruieren
        return self.distance, self.parent


def find_path(parent, start, goal):
    path = []

    # starte mit goalknoten
    x, y = goal

    # zurückverfolgen bis man beim startknoten ankommt
    while (x, y) != start:
        # aktuellen knoten zum pfad hinzufügen
        path.append((x, y))

        # zum parentknoten des aktuellen knotens gehen
        x, y = parent[x][y]

    path.append(start)

    # pfad umkehren >> da aufgebaut von goal zu start
    path.reverse()

    return path
