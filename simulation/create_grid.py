import json
import random
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

class CreateGrid:
    def __init__(self):
        self.size = 0
        self.grid = 0
        self.goal_x = 0
        self.goal_y = 0
        self.agent_x = 0
        self.agent_y = 0

    def add_padding(self):
        padded_grid = [[1] * (self.size + 2) for _ in range(self.size + 2)]
        for i in range(self.size):
            for j in range(self.size):
                padded_grid[i + 1][j + 1] = self.grid[i][j]
        return padded_grid

    def save_grid_to_json(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.grid, f, indent=2)

    def create_empty_grid(self):
        grid = [[0] * self.size for _ in range(self.size)]
        return grid

    def place_agent(self):
        agent_x = random.randint(0, self.size // 8)
        agent_y = random.randint(self.size // 4, 3 * self.size // 4)

        while self.grid[agent_x][agent_y] == 1:
            agent_x = random.randint(1, self.size // 8)
            agent_y = random.randint(self.size // 4, 3 * self.size // 4)
        return agent_x, agent_y

    def place_goal(self):
        goal_x = random.randint(7 * self.size // 8, self.size - 1)
        goal_y = random.randint(self.size // 4, 3 * self.size // 4)

        while self.grid[goal_x][goal_y] == 1:
            goal_x = random.randint(7 * self.size // 8, self.size - 1)
            goal_y = random.randint(self.size // 4, 3 * self.size // 4)
        return goal_x, goal_y

    def get_free_position_in_top_left(self):
        while True:
            x = random.randint(0, self.size // 4 - 1)
            y = random.randint(0, self.size // 4 - 1)

            if self.grid[x][y] == 0:
                return x, y

    def get_free_position_in_bottom_right(self):
        while True:
            x = random.randint(self.size - self.size // 6, self.size - 2)
            y = random.randint(self.size - self.size // 6, self.size - 2)

            if self.grid[x][y] == 0:
                return x, y

    def create_star_grid(self, size, save_grid=False):
        # Erstellen des leeren Grids
        self.size = size
        self.grid = self.create_empty_grid()

        # Dynamische Parameter für das Muster
        # Unten rechts (l1)
        l1_x = self.size - self.size // 3
        l1_y = self.size - self.size // 4
        l1_length = self.size // 4
        l1_thickness = self.size // 10

        for x in range(l1_x, min(l1_x + l1_length, size)):
            for y in range(l1_y, min(l1_y + l1_thickness, size)):
                self.grid[x][y] = 1

        for x in range(l1_x, min(l1_x + l1_thickness, size)):
            for y in range(l1_y, min(l1_y + l1_length, size)):
                self.grid[x][y] = 1

        # Oben links (l2)
        l2_x = size // 10
        l2_y = size // 5
        l2_length = size // 4
        l2_thickness = size // 10

        for x in range(l2_x, min(l2_x + l2_length, size)):
            for y in range(l2_y, min(l2_y + l2_thickness, size)):
                self.grid[x][y] = 1

        for x in range(l2_x + l2_length - l2_thickness, min(l2_x + l2_length, size)):
            for y in range(l2_y, min(l2_y - l2_length, size), - 1):
                self.grid[x][y] = 1

        self.grid = self.add_padding()

        # Bestimmen der Positionen für Agent und Ziel
        agent_x, agent_y = self.get_free_position_in_top_left()
        goal_x, goal_y = self.get_free_position_in_bottom_right()

        # Grid speichern, wenn der Parameter aktiviert ist
        if save_grid:
            save_grid_to_file({
                "name": "detour",
                "agent_x": agent_x,
                "agent_y": agent_y,
                "goal_x": goal_x,
                "goal_y": goal_y,
                "size": size,
                "grid": self.grid
            })

        # Rückgabe des Grids mit Metadaten
        return {
            "name": "detour",
            "agent_x": agent_x,
            "agent_y": agent_y,
            "goal_x": goal_x,
            "goal_y": goal_y,
            "size": size,
            "grid": self.grid
        }

    def create_simple_grid(self, size, save_grid=False):
        # Erstellen eines leeren Grids
        self.size = size
        self.grid = self.create_empty_grid()

        num_rect = min(2, self.size // 15)

        rectangles = []
        for _ in range(num_rect):
            max_attempts = 100  # Verhindert Endlosschleifen
            attempts = 0
            while attempts < max_attempts:
                # Dimensionen der Rechtecke proportional zur Größe des Grids
                rect_width = random.randint(size // 10, size // 4)
                rect_height = random.randint(size // 10, size // 4)

                # Positionen der Rechtecke innerhalb des zentralen Bereichs des Grids
                rect_x = random.randint(size // 4, 3 * size // 4 - rect_width - 1)
                rect_y = random.randint(size // 4, 3 * size // 4 - rect_height - 1)

                # Überprüfen, ob das Rechteck keinen anderen Rechtecken zu nahe kommt
                valid_position = True
                for existing_rect in rectangles:
                    ex_x, ex_y, ex_width, ex_height = existing_rect

                    # Prüfen auf Überschneidung mit einem Puffer von 1 Pixel
                    if not (rect_x >= ex_x + ex_width + 1 or  # rechts vom bestehenden Rechteck
                            rect_x + rect_width + 1 <= ex_x or  # links vom bestehenden Rechteck
                            rect_y >= ex_y + ex_height + 1 or  # unterhalb des bestehenden Rechtecks
                            rect_y + rect_height + 1 <= ex_y):  # oberhalb des bestehenden Rechtecks
                        valid_position = False
                        break

                if valid_position:
                    rectangles.append((rect_x, rect_y, rect_width, rect_height))

                    # Rechteck im Grid markieren
                    for x in range(rect_x, rect_x + rect_width):
                        for y in range(rect_y, rect_y + rect_height):
                            self.grid[x][y] = 1

                    break

                attempts += 1

            if attempts == max_attempts:
                print("Hindernis konnte nicht platziert werden")

        self.grid = self.add_padding()

        agent_x, agent_y = self.place_agent()
        goal_x, goal_y = self.place_goal()


        # Grid speichern, wenn der Parameter aktiviert ist
        if save_grid:
            save_grid_to_file({
                "name": "detour",
                "agent_x": agent_x,
                "agent_y": agent_y,
                "goal_x": goal_x,
                "goal_y": goal_y,
                "size": size,
                "grid": self.grid
            })

        # Rückgabe des Grids mit Metadaten
        return {
            "name": "detour",
            "agent_x": agent_x,
            "agent_y": agent_y,
            "goal_x": goal_x,
            "goal_y": goal_y,
            "size": size,
            "grid": self.grid
        }

    def create_bottleneck_grid(self, size, save_grid=False):
        self.size = size
        self.grid = self.create_empty_grid()

        # Blockierter Balken
        balken_x = size // 3  # Position des Balkens
        balken_dicke = max(1, size // 2)  # Dicke des Balkens proportional zur Größe

        for y in range(size):
            for x in range(balken_x, balken_x + balken_dicke):
                self.grid[x][y] = 1

        bottleneck_width_top = max(1, size // 12)  # Enger Bereich oben
        bottleneck_width_bottom = max(1, size // 6)  # Breiterer Bereich unten
        bottleneck_y_center = size // 2  # Zentrale Position des Weges

        # Obere schmale Passage
        for y in range(bottleneck_y_center - bottleneck_width_top // 2,
                       bottleneck_y_center + (bottleneck_width_top + 1) // 2):
            for x in range(balken_x, balken_x + balken_dicke // 2):
                if 0 <= y < size:
                    self.grid[x][y] = 0

        # Untere breitere Passage
        for y in range(bottleneck_y_center - bottleneck_width_bottom // 2,
                       bottleneck_y_center + (bottleneck_width_bottom + 1) // 2):
            for x in range(balken_x + balken_dicke // 2, balken_x + balken_dicke):
                if 0 <= y < size:
                    self.grid[x][y] = 0

        self.grid = self.add_padding()

        agent_x, agent_y = self.place_agent()
        goal_x, goal_y = self.place_goal()

        # Grid speichern, wenn der Parameter aktiviert ist
        if save_grid:
            save_grid_to_file({
                "name": "detour",
                "agent_x": agent_x,
                "agent_y": agent_y,
                "goal_x": goal_x,
                "goal_y": goal_y,
                "size": size,
                "grid": self.grid
            })

        # Rückgabe des Grids mit Metadaten
        return {
            "name": "detour",
            "agent_x": agent_x,
            "agent_y": agent_y,
            "goal_x": goal_x,
            "goal_y": goal_y,
            "size": size,
            "grid": self.grid
        }

    def create_trap_grid(self, size, save_grid=False):
        self.size = size
        self.grid = self.create_empty_grid()

        # Definieren der Rechtecksgrenzen dynamisch basierend auf der Größe
        rect_start_x = size // 5
        rect_start_y = size // 5
        rect_end_x = size - size // 5
        rect_end_y = size - size // 5

        # Rechteck zeichnen
        for x in range(rect_start_x, rect_end_x):
            for y in range(rect_start_y, rect_end_y):
                self.grid[x][y] = 1

        # Dynamisches Loch innerhalb des Rechtecks erstellen (Buchtform)
        hole_width = random.randint((rect_end_y - rect_start_y) // 3, (rect_end_y - rect_start_y) // 2)
        hole_height = random.randint((rect_end_x - rect_start_x) // 4, (rect_end_x - rect_start_x) // 2)

        # Loch mittig am oberen Rand des Rechtecks platzieren
        hole_start_x = rect_start_x
        hole_start_y = rect_start_y + (rect_end_y - rect_start_y - hole_width) // 2  # Loch beginnt oben am Rechteck

        for x in range(hole_start_x, hole_start_x + hole_width):
            for y in range(hole_start_y, hole_start_y + hole_height):
                if rect_start_x <= x < rect_end_x and rect_start_y <= y < rect_end_y:
                    if random.random() > 0.1:
                        self.grid[x][y] = 0

        self.grid = self.add_padding()

        # Position des Agenten (oben im Grid, außerhalb des Rechtecks)
        agent_x, agent_y = self.place_agent()

        # Position des Ziels (unten im Grid, außerhalb des Rechtecks)
        goal_x, goal_y = self.place_goal()

        # Grid speichern, wenn der Parameter aktiviert ist
        if save_grid:
            save_grid_to_file({
                "name": "detour",
                "agent_x": agent_x,
                "agent_y": agent_y,
                "goal_x": goal_x,
                "goal_y": goal_y,
                "size": size,
                "grid": self.grid
            })

        # Rückgabe des Grids mit Metadaten
        return {
            "name": "detour",
            "agent_x": agent_x,
            "agent_y": agent_y,
            "goal_x": goal_x,
            "goal_y": goal_y,
            "size": size,
            "grid": self.grid
        }

    def create_doubletrap_grid(self, size, save_grid=False):
        self.size = size
        self.grid = self.create_empty_grid()


        # Dynamische Rechtecksgrenzen basierend auf der Größe
        rect_start_x = size // 5
        rect_start_y = size // 5
        rect_end_x = size - size // 5
        rect_end_y = size - size // 5

        # Rechteck zeichnen
        for x in range(rect_start_x, rect_end_x):
            for y in range(rect_start_y, rect_end_y):
                self.grid[x][y] = 1

        # Erste Falle dynamisch erstellen
        hole_width = random.randint((rect_end_y - rect_start_y) // 4, (rect_end_y - rect_start_y) // 2)
        hole_height = random.randint((rect_end_x - rect_start_x) // 4, (rect_end_x - rect_start_x) // 2)

        # Loch mittig am oberen Rand des Rechtecks platzieren
        hole_start_x = rect_start_x
        hole_start_y = rect_start_y + (rect_end_y - rect_start_y - hole_width) // 2  # Loch beginnt oben am Rechteck

        for x in range(hole_start_x, hole_start_x + hole_width):
            for y in range(hole_start_y, hole_start_y + hole_height):
                if rect_start_x <= x < rect_end_x and rect_start_y <= y < rect_end_y:
                    self.grid[x][y] = 0

        # Zweite Falle (gespiegelt) dynamisch erstellen
        hole_start_x_mirror = rect_end_x - (hole_start_x + hole_width - rect_start_x)
        hole_start_y_mirror = rect_end_y - (hole_start_y + hole_height - rect_start_y)
        hole_width_mirror = hole_width
        hole_height_mirror = hole_height

        for x in range(hole_start_x_mirror, hole_start_x_mirror + hole_width_mirror):
            for y in range(hole_start_y_mirror, hole_start_y_mirror + hole_height_mirror):
                if rect_start_x <= x < rect_end_x and rect_start_y <= y < rect_end_y:
                    self.grid[x][y] = 0

        self.grid = self.add_padding()

        # Position des Agenten (oben im Grid, außerhalb des Rechtecks)
        agent_x, agent_y = self.place_agent()

        # Position des Ziels (unten im Grid, außerhalb des Rechtecks)
        goal_x, goal_y = self.place_goal()

        # Grid speichern, wenn der Parameter aktiviert ist
        if save_grid:
            save_grid_to_file({
                "name": "detour",
                "agent_x": agent_x,
                "agent_y": agent_y,
                "goal_x": goal_x,
                "goal_y": goal_y,
                "size": size,
                "grid": self.grid
            })

        # Rückgabe des Grids mit Metadaten
        return {
            "name": "detour",
            "agent_x": agent_x,
            "agent_y": agent_y,
            "goal_x": goal_x,
            "goal_y": goal_y,
            "size": size,
            "grid": self.grid
        }

    def create_detour_grid(self, size, save_grid=False):  ## funzt noch ned auf 16 byye
        self.size = size
        self.grid = self.create_empty_grid()

        # Definieren der Rechtecksgrenzen für die Hindernisse oben und unten
        rect_start_x = size // 5
        rect_start_y = 0
        rect_end_x = size - size // 5
        rect_end_y = size - size // 5

        # Rechtecke zeichnen
        for x in range(rect_start_x, rect_end_x):
            for y in range(rect_start_y, rect_end_y):
                self.grid[x][y] = 1

        # Vertikales Zickzack-Muster innerhalb des Rechtecks
        zickzack_depth = (rect_end_y - rect_start_y) // 4  # Tiefe der Zickzack-Spitzen
        zickzack_width = (rect_end_x - rect_start_x) // 7  # Breite der Zickzack-Abschnitte

        for i in range(10):
            center_y = rect_start_y + (rect_end_y - rect_start_y) // 3
            if i % 2 == 0:  # Zick (nach links in das Hindernis)
                for x in range(rect_start_x + i * zickzack_width, rect_start_x + (i + 1) * zickzack_width):
                    y_spike = center_y - zickzack_depth // 2
                    self.grid[x][y_spike] = 0  # Spitze
                    self.grid[x + 1][y_spike] = 0
                for y in range(center_y - zickzack_depth // 2, center_y + zickzack_depth // 2):
                    self.grid[rect_start_x + i * zickzack_width][y] = 0
            else:  # Zack (nach rechts in das Hindernis)
                for x in range(rect_start_x + i * zickzack_width, rect_start_x + (i + 1) * zickzack_width):
                    y_spike = center_y + zickzack_depth // 2
                    self.grid[x][y_spike] = 0  # Spitze
                    self.grid[x + 1][y_spike - 1] = 0
                for y in range(center_y - zickzack_depth // 2, center_y + zickzack_depth // 2):
                    self.grid[rect_start_x + i * zickzack_width][y] = 0

        self.grid = self.add_padding()

        # Position des Agenten (oben links im Zickzack-Bereich)
        agent_x, agent_y = self.place_agent()
        agent_y = agent_y // 4

        # Position des Ziels (unten rechts im Zickzack-Bereich)
        goal_x, goal_y = self.place_goal()
        goal_y = goal_y // 4

        # Grid speichern, wenn der Parameter aktiviert ist
        if save_grid:
            save_grid_to_file({
                "name": "detour",
                "agent_x": agent_x,
                "agent_y": agent_y,
                "goal_x": goal_x,
                "goal_y": goal_y,
                "size": size,
                "grid": self.grid
            })

        # Rückgabe des Grids mit Metadaten
        return {
            "name": "detour",
            "agent_x": agent_x,
            "agent_y": agent_y,
            "goal_x": goal_x,
            "goal_y": goal_y,
            "size": size,
            "grid": self.grid
        }

    def create_base_grid(self, size, save_grid=False):
        self.size = size
        self.grid = self.create_empty_grid()

        self.grid = self.add_padding()

        # Position des Agenten
        agent_x, agent_y = self.place_agent()

        # Position des Ziels
        goal_x, goal_y = self.place_goal()

        # Grid speichern, wenn der Parameter aktiviert ist
        if save_grid:
            save_grid_to_file({
                "name": "detour",
                "agent_x": agent_x,
                "agent_y": agent_y,
                "goal_x": goal_x,
                "goal_y": goal_y,
                "size": size,
                "grid": self.grid
            })

        # Rückgabe des Grids mit Metadaten
        return {
            "name": "detour",
            "agent_x": agent_x,
            "agent_y": agent_y,
            "goal_x": goal_x,
            "goal_y": goal_y,
            "size": size,
            "grid": self.grid
        }

    def create_grid(self, grid:str, size, save_grid=False):
        if grid == 'empty':
            return self.create_base_grid(size, save_grid)
        elif grid == 'star_grid':
            return self.create_star_grid(size, save_grid)
        elif grid == 'simple_grid':
            return self.create_simple_grid(size, save_grid)
        elif grid == 'bottleneck_grid':
            return self.create_bottleneck_grid(size, save_grid)
        elif grid == 'trap_grid':
            return self.create_trap_grid(size, save_grid)
        elif grid == 'doubletrap_grid':
            return self.create_doubletrap_grid(size, save_grid)
        elif grid == 'detour_grid':
            return self.create_detour_grid(size, save_grid)