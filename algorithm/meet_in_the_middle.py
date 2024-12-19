from collections import deque


class MeetInTheMiddleAlgorithm:
    def __init__(self, grid, start, goal):
        self.grid = grid
        self.start = start
        self.goal = goal

    def meet_in_the_middle(self):
        # anzahl zeilen und spalten bestimmen
        rows, cols = len(self.grid), len(self.grid[0])

        # start- und goalkoordinaten extrahiern
        (agent_x, agent_y) = self.start
        (goal_x, goal_y) = self.goal

        # falls start oder goal blockiert >> fehler
        if self.grid[agent_x][agent_y] or self.grid[goal_x][goal_y]:
            raise ValueError("Start oder Ziel ist blockiert.")

        # init von distanz- und parentinfo für beide suchrichtungen
        distance_from_start = [[float('inf')] * cols for _ in range(rows)]
        distance_from_goal = [[float('inf')] * cols for _ in range(rows)]
        parent_from_start = [[None] * cols for _ in range(rows)]
        parent_from_goal = [[None] * cols for _ in range(rows)]

        # dist zum startpkt und goalpunkt gleich 0 setzen
        distance_from_start[agent_x][agent_y] = 0
        distance_from_goal[goal_x][goal_y] = 0

        # bfs queue für start- und goal-richtungen
        queue_start = deque([(agent_x, agent_y)])
        queue_goal = deque([(goal_x, goal_y)])

        # bfs solange queue nicht leer
        while queue_start and queue_goal:
            # expandieren von start aus
            if queue_start:
                x, y = queue_start.popleft()
                # alle möglichen nachbarn in die 4 richtungen
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    # prüfen ob nachbar im grid und frei (inf)
                    if 0 <= nx < rows and 0 <= ny < cols:
                        if not self.grid[nx][ny] and distance_from_start[nx][ny] == float('inf'):
                            distance_from_start[nx][ny] = distance_from_start[x][y] + 1
                            parent_from_start[nx][ny] = (x, y)
                            queue_start.append((nx, ny))
                            # treffen sie sich
                            if distance_from_goal[nx][ny] != float('inf'):
                                return self.find_path(parent_from_start, parent_from_goal, (nx, ny), self.start,
                                                      self.goal)

            # expandieren von goal aus
            if queue_goal:
                x, y = queue_goal.popleft()
                # alle möglichen nachbarn in die 4 richtungen
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    # prüfen on nachbar innerhalb des grids und frei (inf)
                    if 0 <= nx < rows and 0 <= ny < cols:
                        if not self.grid[nx][ny] and distance_from_goal[nx][ny] == float('inf'):
                            distance_from_goal[nx][ny] = distance_from_goal[x][y] + 1
                            parent_from_goal[nx][ny] = (x, y)
                            queue_goal.append((nx, ny))
                            # treffen sie sich
                            if distance_from_start[nx][ny] != float('inf'):
                                return self.find_path(parent_from_start, parent_from_goal, (nx, ny), self.start,
                                                      self.goal)

        # kein pfad gefunden
        return None

    def find_path(self, parent_from_start, parent_from_goal, meet_point, start, goal):
        (meeting_p_x, meeting_p_y) = meet_point

        # pfad von start zu meetingpoint rekonstruieren
        path_from_start = []
        x, y = meeting_p_x, meeting_p_y
        while (x, y) != start:
            if parent_from_start[x][y] is None:
                raise ValueError(f"Kein Parent für Knoten {(x, y)} vom Start aus gefunden.")
            x, y = parent_from_start[x][y]
            path_from_start.append((x, y))
        path_from_start.reverse()

        # pfad vom meetingpoint zum goal rekonstruieren
        path_from_goal = []
        x, y = meeting_p_x, meeting_p_y
        while (x, y) != goal:
            if parent_from_goal[x][y] is None:
                raise ValueError(f"Kein Parent für Knoten {(x, y)} vom Goal aus gefunden.")
            x, y = parent_from_goal[x][y]
            path_from_goal.append((x, y))

        # ganzer pfad
        return path_from_start + [(meeting_p_x, meeting_p_y)] + path_from_goal
