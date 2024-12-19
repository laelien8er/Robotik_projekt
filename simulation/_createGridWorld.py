# initial Code from https://minigrid.farama.org/content/create_env_tutorial/
from __future__ import annotations
import json
import numpy as np
from minigrid.core.grid import Grid
from minigrid.core.mission import MissionSpace
from minigrid.core.world_object import Goal, Wall
from minigrid.minigrid_env import MiniGridEnv


class GridEnv(MiniGridEnv):

    def __init__(
            self,
            agent_start_dir=0,
            max_steps: int | None = None, # default 4 * size ** 2
            map_file: str = False,
            **kwargs,
    ):
        # initialize grid from json file
        with open(map_file, 'r') as file:
            self.map_data = json.load(file)
            size = self.map_data["size"]
            agent_start_pos = (self.map_data["agent_x"], self.map_data["agent_y"])

        self.agent_start_pos = agent_start_pos
        self.agent_start_dir = agent_start_dir

        mission_space = MissionSpace(mission_func=self._gen_mission)

        if max_steps is None:
            max_steps = 4 * size ** 2

        super().__init__(
            mission_space=mission_space,
            grid_size=size,
            see_through_walls=True,
            max_steps=max_steps,
            **kwargs
        )

    @staticmethod
    def _gen_mission():
        return "test"

    def _gen_grid(self, width, height):
        # Create an empty grid
        self.grid = Grid(width, height)

        # Generate the surrounding walls
        self.grid.wall_rect(0, 0, width, height)

        # Generate walls
        for i in self.get_coordinates():
            self.grid.set(i[1], i[0], Wall())

        # Place goal
        self.put_obj(Goal(), self.map_data["goal_x"] , self.map_data["goal_y"])

        # Place agent
        if self.agent_start_pos is not None:
            self.agent_pos = self.agent_start_pos
            self.agent_dir = self.agent_start_dir
        else:
            self.place_agent()

        self.mission = self.map_data["name"]

    def get_coordinates(self):
        grid = np.array(self.map_data["grid"]).astype(int)
        if np.shape(grid)[0] < self.map_data["size"] - 1:
            pad_n = self.map_data["size"] - np.shape(grid)[0] - 2
            grid = np.pad(grid, pad_n, mode="constant")
        return np.argwhere(grid == 1)



