import time
from algorithm import AStarAlgorithm
import json
import pandas as pd
import numpy as np

#ToDo: create benchmark names
benchmarks = ['test']

class Metrics:
    def __init__(self):
        pass

    def get_metrics(self, algorithm: str = False, num_runns: int = 10):
        alg = None

        measurements = pd.DataFrame(columns=['benchmark', 'avg_time', 'avg_path_length', 'avg_steps_to_converge'])

        if algorithm == 'A-stern':
            alg = AStarAlgorithm()

        # ToDo
        # elif algorithm == 'Wavefront':
        #     alg =
        # elif algorithm == tbd:
        #     alg =
        else:
            print(f"Algorithm {algorithm} not found")

        # measurements for each algorithm
        all_times = []
        all_path_lengths =[]
        all_steps = []

        for b in benchmarks:
            times = []
            path_lengths = []
            steps = []

            for i in range(num_runns):
                # ToDo: initalize dynamic grids
                start, end, grid = dummy_grid_generation(benchmark=b)

                s = time.perf_counter()
                path, step = alg.find_path(start, end, grid)

                # returns false if no path could be found
                if not path:
                    continue

                e = time.perf_counter()
                time_used = e - s

                times.append(time_used)
                path_lengths.append(len(path))
                steps.append(steps)

            all_times.extend(times)
            all_path_lengths.extend(path_lengths)
            all_steps.extend(steps)

            row = pd.DataFrame([[b,
                                 f'{np.mean(times):.5f}±{np.std(times):.5f}',
                                 f'{np.mean(path_lengths)}±{np.std(path_lengths)}',
                                 f'{np.mean(steps)}±{np.std(steps)}',
                                 ]], columns=measurements.columns)
            measurements = pd.concat([measurements, row], ignore_index=True)

        row = pd.DataFrame([['all',
                             f'{np.mean(all_times):.5f}±{np.std(all_times):.5f}',
                             f'{np.mean(all_path_lengths)}±{np.std(all_path_lengths)}',
                             f'{np.mean(all_steps)}±{np.std(all_steps)}',
                             ]], columns=measurements.columns)
        measurements = pd.concat([measurements, row], ignore_index=True)

        # ToDo: create show grid
        start, end, grid = dummy_grid_generation(benchmark='show')
        path = alg.find_path(start, end, grid)

        return path, len(grid[0]), measurements


def dummy_grid_generation(benchmark: str):

    if benchmark == 'test' or benchmark == 'show':
        file_path = "/home/lea/Dokumente/WS24_25/Robotik_projekt/simulation/grid_test.json"

    with open(file_path, 'r') as file:
        map_data = json.load(file)

    start = (map_data['agent_x'], map_data['agent_y'])
    end = (map_data['goal_x'], map_data['goal_y'])
    grid = map_data['grid']

    return start, end, grid

