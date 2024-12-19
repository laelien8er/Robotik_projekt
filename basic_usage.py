from algorithm import AStarAlgorithm
import json
from minigrid.manual_control import ManualControl
from minigrid.wrappers import RGBImgPartialObsWrapper, ImgObsWrapper

from simulation import GridWorldEnv



# get grid details
file_path = "/home/lea/Dokumente/WS24_25/Robotik_projekt/simulation/grid_test.json"

# neues grid
env = GridWorldEnv(render_mode="human", map_path=file_path)


# altes grid:
# env = GridEnv(render_mode="human" , map_file=file_path)
observation, info = env.reset()


# with open(file_path, 'r') as file:
#     map_data = json.load(file)
#
# start = (map_data['agent_x'], map_data['agent_y'])
# end = (map_data['goal_x'], map_data['goal_y'])
# grid = map_data['grid']
#
# p = AStarAlgorithm(start, end, grid).find_path()
# print(p)


# # enable manual control for testing
# manual_control = ManualControl(env, seed=42)
# manual_control.start()

#
# sample actions
episode_over = False
while not episode_over:
    action = env.action_space.sample()  # agent policy that uses the observation and info
    observation, reward, terminated, truncated, info = env.step(action)

    episode_over = terminated or truncated

env.close()


