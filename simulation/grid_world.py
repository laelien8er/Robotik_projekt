from enum import Enum
import gymnasium as gym
from gymnasium import spaces
import pygame
import numpy as np
import json


class Actions(Enum):
    right = 0
    up = 1
    left = 2
    down = 3


class GridWorldEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}
    OBSTACLE: int = 1

    def __init__(self, render_mode=None,
                 size=5,
                 agent = None,
                 goal = None,
                 grid = None,
                 map_path = None):

        if map_path:
            with open(map_path, 'r') as file:
                map_data = json.load(file)
                size = map_data["size"]
                agent = (map_data["agent_x"], map_data["agent_y"])
                goal = (map_data["goal_x"], map_data["goal_y"])
                grid = map_data["grid"]

        self.size = size  # The size of the square grid
        self.window_size = 512  # The size of the PyGame window
        self.agent = agent # Start coordinates of agent (x,y)
        self.goal = goal # coordinates of goal (x,y)
        self.grid = grid # array of grid

        np_grid  = np.array(self.grid).astype(int)
        self.locs_obstacles = np.argwhere(np_grid == 1)

        # Observations are dictionaries with the agent's and the target's location.
        # Each location is encoded as an element of {0, ..., `size`}^2,
        # i.e. MultiDiscrete([size, size]).
        self.observation_space = spaces.Dict(
            {
                "agent": spaces.Box(0, size - 1, shape=(2,), dtype=int),
                "target": spaces.Box(0, size - 1, shape=(2,), dtype=int),
            }
        )

        # We have 4 actions, corresponding to "right", "up", "left", "down", "right"
        self.action_space = spaces.Discrete(4)

        """
        The following dictionary maps abstract actions from `self.action_space` to 
        the direction we will walk in if that action is taken.
        i.e. 0 corresponds to "right", 1 to "up" etc.
        """
        self._action_to_direction = {
            Actions.right.value: np.array([1, 0]),
            Actions.up.value: np.array([0, 1]),
            Actions.left.value: np.array([-1, 0]),
            Actions.down.value: np.array([0, -1]),
        }

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        """
        If human-rendering is used, `self.window` will be a reference
        to the window that we draw to. `self.clock` will be a clock that is used
        to ensure that the environment is rendered at the correct framerate in
        human-mode. They will remain `None` until human-mode is used for the
        first time.
        """
        self.window = None
        self.clock = None

    def _get_obs(self):
        return {"agent": self._agent_location, "target": self._target_location}

    def _get_info(self):
        return {
            "distance": np.linalg.norm(
                self._agent_location - self._target_location, ord=1
            )
        }

    def reset(self, seed=None, options=None):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)

        # Choose the agent's location uniformly at random
        self._agent_location = np.array([self.agent[0], self.agent[1]])

        # We will sample the target's location randomly until it does not
        # coincide with the agent's location
        self._target_location = np.array([self.goal[0], self.goal[1]])
        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, info

    def step(self, action):
        # Map the action (element of {0,1,2,3}) to the direction we walk in
        direction = self._action_to_direction[action]
        # We use `np.clip` to make sure we don't leave the grid

        # check if the agent hit obstical
        hit_obstacle = False
        next = self._agent_location + direction
        next_loc = np.array([next[1], next[0]])
        if next_loc.tolist() in self.locs_obstacles.tolist():
            self._agent_location = self._agent_location
            hit_obstacle= True
        else:
            self._agent_location = np.clip(
                self._agent_location + direction, 0, self.size - 1
            )
        # An episode is done if the agent has reached the target
        terminated = np.array_equal(self._agent_location, self._target_location)

        # Rewards
        if terminated:
            reward = 100
        elif hit_obstacle:
            # get small punishment if obstical is hit
            reward = -5
        else:
            reward = -1

        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, reward, terminated, False, info

    def render(self):
        if self.render_mode == "rgb_array":
            return self._render_frame()

    def _render_frame(self):
        if self.window is None and self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode((self.window_size, self.window_size))
        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()

        canvas = pygame.Surface((self.window_size, self.window_size))
        canvas.fill((241, 226, 226))
        pix_square_size = (
            self.window_size / self.size
        )  # The size of a single grid square in pixels

        # First we draw the target
        pygame.draw.rect(
            canvas,
            (198, 133, 141),
            pygame.Rect(
                pix_square_size * self._target_location,
                (pix_square_size, pix_square_size),
            ),
        )
        # Now we draw the agent
        pygame.draw.circle(
            canvas,
            (188, 162, 170),
            (self._agent_location + 0.5) * pix_square_size,
            pix_square_size / 3,
        )

        # draw obstacles
        for loc in self.locs_obstacles:
            pygame.draw.rect(
                canvas,
                (232, 175, 148),
                pygame.Rect(
                    pix_square_size * np.array([loc[1], loc[0]]),
                    (pix_square_size, pix_square_size),
                ),
            )

        # Finally, add some gridlines
        for x in range(self.size + 1):
            pygame.draw.line(
                canvas,
                (220,204,165),
                (0, pix_square_size * x),
                (self.window_size, pix_square_size * x),
                width=3,
            )
            pygame.draw.line(
                canvas,
                (220,204,165),
                (pix_square_size * x, 0),
                (pix_square_size * x, self.window_size),
                width=3,
            )

        if self.render_mode == "human":
            # The following line copies our drawings from `canvas` to the visible window
            self.window.blit(canvas, canvas.get_rect())
            pygame.event.pump()
            pygame.display.update()

            # We need to ensure that human-rendering occurs at the predefined framerate.
            # The following line will automatically add a delay to
            # keep the framerate stable.
            self.clock.tick(self.metadata["render_fps"])
        else:  # rgb_array
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(canvas)), axes=(1, 0, 2)
            )

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()
