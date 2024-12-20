import time
import pandas as pd
import numpy as np
from algorithm import AStarAlgorithm, WavefrontAlgorithm, MeetInTheMiddleAlgorithm

from simulation import CreateGrid

benchmarks = ['empty', 'star_grid', 'simple_grid', 'bottleneck_grid', 'trap_grid', 'doubletrap_grid', 'detour_grid']


class Metrics:

    def get_metrics(self, algorithm: str = False, size_grid: int = 32, num_runs: int = 5):
        alg = None

        measurements = pd.DataFrame(columns=['benchmark', 'avg_time (sec)', 'avg_path_length', 'avg_steps_to_converge'
                                                                                               'avg_distance'])

        # measurements for each algorithm
        all_times = []
        all_path_lengths = []
        all_steps = []
        all_distances = []

        if algorithm == 'A-star':
            alg = AStarAlgorithm()
        elif algorithm == 'Wavefront':
            alg = WavefrontAlgorithm()
        elif algorithm == 'MITM':
            alg = MeetInTheMiddleAlgorithm()
        else:
            print(f"Algorithm {algorithm} not found")
            return False

        for b in benchmarks:
            times = []
            path_lengths = []
            steps = []
            distances = []

            for i in range(num_runs):
                grid_creator = CreateGrid()
                grid_dict = grid_creator.create_grid(b, size_grid)

                start = (grid_dict['agent_x'], grid_dict['agent_y'])
                end = (grid_dict['goal_x'], grid_dict['goal_y'])
                grid = grid_dict['grid']

                s = time.perf_counter()
                path, step_used = alg.find_path(start, end, grid)
                avg_distance = self.average_distance_to_obstacles(path, grid)

                # returns false if no path could be found
                if not path:
                    continue
                e = time.perf_counter()
                time_used = e - s

                times.append(time_used)
                path_lengths.append(len(path))
                steps.append(step_used)
                distances.append(avg_distance)

            all_distances.extend(distances)
            all_times.extend(times)
            all_path_lengths.extend(path_lengths)
            all_steps.extend(steps)

            row = pd.DataFrame([[b, times, path_lengths, steps]], columns=measurements.columns)
            measurements = pd.concat([measurements, row], ignore_index=True)

        row = pd.DataFrame([['all', all_times, all_path_lengths, all_steps, all_distances]], columns=measurements.columns)
        measurements = pd.concat([measurements, row], ignore_index=True)

        df_new = measurements.iloc[:, 1:]
        df_mapped = df_new.map(mean_std)
        measurements = pd.concat([measurements.iloc[:, 0], df_mapped], axis=1)

        return measurements

    def average_distance_to_obstacles(self, path, grid):
        # alle blockierten zellen finden
        blocked_indices = np.argwhere(grid)

        if blocked_indices.size == 0:
            # keine hindernisse >> distanz ist unendlich
            return [float('inf') for _ in path]

        distances = []
        for position in path:
            x, y = position
            # sind innerhalb des gitters
            if 0 <= x < grid.shape[0] and 0 <= y < grid.shape[1]:
                # manhatten distanz zu den hindernissen
                dists = np.abs(blocked_indices[:, 0] - x) + np.abs(blocked_indices[:, 1] - y)
                avg_dist = np.mean(dists)
                distances.append(avg_dist)
            else:
                distances.append(float('inf'))
                print("Befindet sich außerhalb des Grids.")

        # durschnitt über den ganzen pfad >> keine unendichen distanzen
        all_distances = [d for d in distances if np.isfinite(d)]
        if all_distances:
            return np.mean(all_distances)
        else:
            return float('inf')


def mean_std(x):
    return f"{np.mean(x):.5f} ± {np.std(x):.5f}"
