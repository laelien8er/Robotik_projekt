# initial code from https://minigrid.farama.org/content/training/

from stable_baselines3.common.torch_layers import BaseFeaturesExtractor
import torch.nn as nn
import torch
import gymnasium as gym


class MinigridFeaturesExtractor(BaseFeaturesExtractor):
    def __init__(self, observation_space: gym.Space, features_dim: int = 512, normalized_image: bool = False) -> None:
        super().__init__(observation_space, features_dim)
        n_input_channels = observation_space.shape[0]
        self.cnn = nn.Sequential(
            nn.Conv2d(n_input_channels, 16, (2, 2)),
            nn.ReLU(),
            nn.Conv2d(16, 32, (2, 2)),
            nn.ReLU(),
            nn.Conv2d(32, 64, (2, 2)),
            nn.ReLU(),
            nn.Flatten(),
        )

        # Compute shape by doing one forward pass
        with torch.no_grad():
            n_flatten = self.cnn(torch.as_tensor(observation_space.sample()[None]).float()).shape[1]

        self.linear = nn.Sequential(nn.Linear(n_flatten, features_dim), nn.ReLU())

    def forward(self, observations: torch.Tensor) -> torch.Tensor:
        return self.linear(self.cnn(observations))

from minigrid.wrappers import ImgObsWrapper
from stable_baselines3 import PPO

policy_kwargs = dict(
    features_extractor_class=MinigridFeaturesExtractor,
    features_extractor_kwargs=dict(features_dim=128),
)



#### Train Agent #####

from simulation import GridEnv
# get grid details
file_path = "/home/lea/Dokumente/WS24_25/Robotik_projekt/simulation/grid_test.json"
env = GridEnv(render_mode="rgb_array", map_file=file_path)
env = ImgObsWrapper(env)

model = PPO("CnnPolicy", env, policy_kwargs=policy_kwargs, verbose=1)
model.learn(total_timesteps=25000)

env = GridEnv(render_mode="human", map_file=file_path)
env = ImgObsWrapper(env)

observation, _ = env.reset()

episode_over = False
while not episode_over:
    action, _ = model.predict(observation)
    observation, reward, terminated, truncated, _ = env.step(action)

    episode_over = terminated or truncated

env.close()



