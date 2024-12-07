from simulation import GridEnv

# get grid details
file_path = "/home/lea/Dokumente/WS24_25/Robotik_projekt/simulation/grid_test.json"

env = GridEnv(render_mode="human" , map_file=file_path)
observation, info = env.reset()

episode_over = False
while not episode_over:
    action = env.action_space.sample()  # agent policy that uses the observation and info
    observation, reward, terminated, truncated, info = env.step(action)

    episode_over = terminated or truncated

env.close()


