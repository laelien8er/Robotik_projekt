import time
import json
import pandas as pd
import numpy as np
from algorithm import AStarAlgorithm

from simulation import CreateGrid

benchmarks = ['empty', 'star_grid', 'simple_grid', 'bottleneck_grid', 'trap_grid', 'doubletrap_grid', 'detour_grid']

class Metrics:
    def __init__(self):
        pass

    def get_metrics(self, algorithm: str = False, size_grid: int = 32, num_runns: int = 5):
        alg = None

        measurements = pd.DataFrame(columns=['benchmark', 'avg_time', 'avg_path_length', 'avg_steps_to_converge'])

        # measurements for each algorithm
        all_times = []
        all_path_lengths =[]
        all_steps = []

        if algorithm == 'A-stern':
            alg = AStarAlgorithm()

        # ToDo
        # elif algorithm == 'Wavefront':
        #     alg =
        # elif algorithm == tbd:
        #     alg =
        else:
            print(f"Algorithm {algorithm} not found")
            return False

        for b in benchmarks:
            times = []
            path_lengths = []
            steps = []

            for i in range(num_runns):
                grid_creator = CreateGrid()
                grid_dict = grid_creator.create_grid(b, size_grid)

                start = (grid_dict['agent_x'], grid_dict['agent_y'])
                end = (grid_dict['goal_x'], grid_dict['goal_y'])
                grid = grid_dict['grid']

                s = time.perf_counter()
                path, step_used = alg.find_path(start, end, grid)
                # returns false if no path could be found
                if not path:
                    continue
                e = time.perf_counter()
                time_used = e - s

                times.append(time_used)
                path_lengths.append(len(path))
                steps.append(step_used)

            all_times.extend(times)
            all_path_lengths.extend(path_lengths)
            all_steps.extend(steps)

            row = pd.DataFrame([[b,times, path_lengths, steps]], columns=measurements.columns)
            measurements = pd.concat([measurements, row], ignore_index=True)

        row = pd.DataFrame([['all', all_times, all_path_lengths, all_steps]], columns=measurements.columns)
        measurements = pd.concat([measurements, row], ignore_index=True)

        return measurements


