from blockworld import BlockWorldEnv
import numpy as np
import random

class EpsilonGreedyPolicy():
  def __init__(self, epsilon):
    self.epsilon = epsilon

  def act(self, akce_dict):
    # epsilon greedy
    if np.random.rand() > self.epsilon:
      a = max(akce_dict, key=akce_dict.get)
    else:
      a = random.choice(list(akce_dict.keys()))

    return a

class QLearning():
	# don't modify the methods' signatures!
	def __init__(self, env: BlockWorldEnv):
		self.env = env
		self.epsilon = 0.9
		self.exploration_policy = EpsilonGreedyPolicy(self.epsilon)
		self.alpha_init = 0.5
		self.gamma = 0.9
		self.goalDict = dict()
		self.episode = 1

	def get_alpha(self):
		return self.alpha_init

	def train(self):
		# Use BlockWorldEnv to simulate the environment with reset() and step() methods.
		for ig in range(73):
			s = self.env.reset()
			while s[1] in self.goalDict:
				s = self.env.reset()

			stavy_dict = dict()

			akce_dict = dict()

			for a in s[0].get_actions():
				akce_dict[a] = 0
			stavy_dict[s[0]] = akce_dict

			for episode in range(50):
				done = False
				while not done:
					next_max = 0
					a = self.exploration_policy.act(stavy_dict[s[0]])
					s_next, reward, done = self.env.step(a)
					if s_next[0] in stavy_dict:
						all_values = stavy_dict[s_next[0]].values()
						q_max = max(all_values)
					else:
						akce_dict = dict()
						for ak in s_next[0].get_actions():
							akce_dict[ak] = 0
						q_max = 0
						stavy_dict[s_next[0]] = akce_dict

					val = self.get_alpha() * (reward + self.gamma * q_max)
					stavy_dict[s[0]][a] = stavy_dict[s[0]][a] + val - self.get_alpha() * stavy_dict[s[0]][a]
					s = s_next
			self.goalDict[s[1]] = stavy_dict
			#print(str(ig)+ "--- " + str(s[1]))

		# s = self.env.reset()
		# s_, r, done = self.env.step(a)

	def act(self, s):
		if s[1] in self.goalDict:
			stavy_dict = self.goalDict[s[1]]
			if s[0] in stavy_dict:
				akce_dict = stavy_dict[s[0]]
				action = max(akce_dict, key=akce_dict.get)
			else:
				action = random.choice(s[0].get_actions())
		else:
			action = random.choice(s[0].get_actions())
		return action

if __name__ == '__main__':
	# Here you can test your algorithm. Stick with N <= 4
	N = 4

	env = BlockWorldEnv(N)
	qlearning = QLearning(env)

	# Train
	qlearning.train()

	# Evaluate
	test_env = BlockWorldEnv(N)

	test_problems = 10
	solved = 0
	avg_steps = []

	for test_id in range(test_problems):
		s = test_env.reset()
		done = False

		print(f"\nProblem {test_id}:")
		print(f"{s[0]} -> {s[1]}")

		for step in range(50): 	# max 50 steps per problem
			a = qlearning.act(s)
			s_, r, done = test_env.step(a)

			print(f"{a}: {s[0]}")

			s = s_

			if done:
				solved += 1
				avg_steps.append(step + 1)
				break

	avg_steps = sum(avg_steps) / len(avg_steps)
	print(f"Solved {solved}/{test_problems} problems, with average number of steps {avg_steps}.")