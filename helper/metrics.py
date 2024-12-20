import time
import json
import pandas as pd
import numpy as np
from algorithm import AStarAlgorithm, WavefrontAlgorithm, MeetInTheMiddleAlgorithm, SASAR, QLearning

from simulation import CreateGrid, GridWorldEnv

benchmarks = ['empty', 'star_grid', 'simple_grid', 'bottleneck_grid', 'trap_grid', 'doubletrap_grid', 'detour_grid']

class Metrics:

    def get_metrics(self, algorithm: str = False, size_grid: int = 32, num_runs: int = 5):
        alg = None

        measurements = pd.DataFrame(columns=['benchmark', 'avg_time (sec)', 'avg_path_length', 'avg_steps_to_converge'])

        # measurements for each algorithm
        all_times = []
        all_path_lengths =[]
        all_steps = []

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

            for i in range(num_runs):
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

        df_new = measurements.iloc[:, 1:]
        df_mapped = df_new.map(mean_std)
        measurements = pd.concat([measurements.iloc[:, 0], df_mapped], axis=1)

        return measurements

    def get_rl_metrics(self,
                       algorithm: str = False,
                       size_grid: int = 32,
                       n_train_epochs = [500,1000,10000],
                       learning_rate: int =0.7,
                       gamma: int = 0.95,
                       max_epsilon: int = 1.0,
                       min_epsilon: int = 0.05,
                       decay_rate: int = 0.0005,
                       n_eval_episodes=100
                       ):

        measurements = pd.DataFrame(columns=['benchmark', 'train_epoch' ,'avg_time_train (sec)', 'mean_reward', 'std_reward'])

        for b in benchmarks:

            for i in n_train_epochs:
                grid_creator = CreateGrid()
                grid_dict = grid_creator.create_grid(b, size_grid)

                env = GridWorldEnv(render_mode="rgb_array", map_dict=grid_dict)

                if algorithm == 'sasar':
                    alg = SASAR(env)
                elif algorithm == 'qlearning':
                    alg = QLearning(env)
                else:
                    print(f"Algorithm {algorithm} not found")
                    return False

                max_steps = alg.n_states * 2

                s = time.perf_counter()
                q_table = alg.train(i,min_epsilon, max_epsilon, decay_rate, max_steps, learning_rate, gamma)
                e = time.perf_counter()
                time_used = e - s

                mean, std  = alg.evaluate_agent(max_steps, n_eval_episodes)

                row = pd.DataFrame([[b, i , time_used, mean, std]], columns=measurements.columns)
                measurements = pd.concat([measurements, row], ignore_index=True)

        return measurements







def mean_std(x):
    return f"{np.mean(x):.5f} ± {np.std(x):.5f}"