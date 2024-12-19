import numpy as np
import gymnasium as gym
import random
import imageio
from tqdm.notebook import trange


class SASAR:
    def __init__(self, env):
        self.env = env
        self.n_states = env.size ** 2
        self.action_space = env.action_space.n
        self.q_table = self.initialize_q_table()

    def get_state(self, state):
        return state[0] * self.env.size + state[1]

    def initialize_q_table(self):
        Qtable = np.zeros((self.n_states, self.action_space))
        return Qtable

    def epsilon_greedy_policy(self, state, epsilon):
        random_int = random.uniform(0, 1)
        if random_int > epsilon:
            action = np.argmax(self.q_table[state])
        else:
            action = self.env.action_space.sample()
        return action

    def train(self,
              n_training_episodes,
              min_epsilon,
              max_epsilon,
              decay_rate,
              max_steps,
              learning_rate,
              gamma):

        for episode in trange(n_training_episodes):
            epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-decay_rate * episode)

            # Reset the environment
            observation, _ = self.env.reset()
            state = self.get_state(observation['agent'])
            step = 0
            done = False
            # choose initial action
            action = self.epsilon_greedy_policy(state, epsilon)

            # repeat
            for step in range(max_steps):

                observation, reward, done, _, _ = self.env.step(action)
                new_state = self.get_state(observation['agent'])
                new_action = self.epsilon_greedy_policy(new_state, epsilon)

                self.q_table[state][action] = self.q_table[state][action] + learning_rate * (
                        reward + gamma * self.q_table[new_state][new_action] - self.q_table[state][action])

                # If done, finish the episode
                if done:
                    break

                # Our state is the new state
                state = new_state
                action = new_action
        return self.q_table

    def evaluate_agent(self, max_steps, n_eval_episodes, seed=None):
        episode_rewards = []
        for episode in range(n_eval_episodes):#
            path = []
            if seed:
                observation, _ = self.env.reset(seed=seed[episode])
                state = self.get_state(observation['agent'])

            else:
                observation, _ = self.env.reset()
                state = self.get_state(observation['agent'])

            step = 0
            done = False
            total_rewards_ep = 0

            for step in range(max_steps):
                # Take the action (index) that have the maximum reward
                action = np.argmax(self.q_table[state][:])
                observation, reward, done, _, _ = self.env.step(action)
                path.append(observation['agent'].tolist())
                new_state = self.get_state(observation['agent'])

                total_rewards_ep += reward

                if done:
                    break
                state = new_state
            episode_rewards.append(total_rewards_ep)
        mean_reward = np.mean(episode_rewards)
        std_reward = np.std(episode_rewards)

        # path is last path generated
        return mean_reward, std_reward, path





