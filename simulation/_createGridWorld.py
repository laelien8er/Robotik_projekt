# initial Code from https://minigrid.farama.org/content/create_env_tutorial/

from __future__ import annotations
import json
import numpy as np
from minigrid.core.grid import Grid
from minigrid.core.mission import MissionSpace
from minigrid.core.world_object import Goal, Wall
from minigrid.manual_control import ManualControl
from minigrid.minigrid_env import MiniGridEnv

# get grid details
file_path = "/home/lea/Dokumente/WS24_25/Robotik_projekt/simulation/grid_test.json"

with open (file_path, 'r') as file:
    map_data = json.load(file)

def get_coordinates():
    grid = np.array(map_data["grid"]).astype(int)
    if np.shape(grid)[0] < map_data["size"]-1:
        pad_n = map_data["size"] - np.shape(grid)[0] - 2
        grid = np.pad(grid, pad_n, mode="constant")
    return np.argwhere(grid==1)


class GridEnv(MiniGridEnv):
    def __init__(
            self,
            size=map_data["size"],
            agent_start_pos=(map_data["agent_x"], map_data["agent_x"]),
            agent_start_dir=0,
            max_steps: int | None = None,
            **kwargs,
    ):
        self.agent_start_pos = agent_start_pos
        self.agent_start_dir = agent_start_dir

        mission_space = MissionSpace(mission_func=self._gen_mission)

        if max_steps is None:
            max_steps = 4 * size ** 2

        super().__init__(
            mission_space=mission_space,
            grid_size=size,
            # Set this to True for maximum speed
            see_through_walls=True,
            max_steps=max_steps,
            **kwargs
        )

    @staticmethod
    def _gen_mission():
        return map_data["name"]

    def _gen_grid(self, width, height):
        # Create an empty grid
        self.grid = Grid(width, height)

        # Generate the surrounding walls
        self.grid.wall_rect(0, 0, width, height)

        # Generate vertical separation wall
        for i in get_coordinates():
            self.grid.set(i[1], i[0], Wall())

        # Place a goal square in the bottom-right corner
        self.put_obj(Goal(), map_data["goal_x"] , map_data["goal_y"])

        # Place the agent
        if self.agent_start_pos is not None:
            self.agent_pos = self.agent_start_pos
            self.agent_dir = self.agent_start_dir
        else:
            self.place_agent()

        self.mission = map_data["name"]


# call in other files with
# from simulation import GridEnv
# from minigrid.manual_control import ManualControl
# env = GridEnv(render_mode="human")
# # enable manual control for testing
# manual_control = ManualControl(env, seed=42)
# manual_control.start()

