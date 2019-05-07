#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 19-5-7 下午5:53
@File    : openai_gym_demo.py
@contact : mmmaaaggg@163.com
@desc    : http://www.zhuanzhi.ai/document/4dfbd65fde2a96c32529538aea15fcfe
通过使用近端策略优化(Proximal Policy Optimization, PPO)算法训练OpenAI Gym中倒立摆来初识TensorForce的简洁和强大

"""
from tensorforce.agents import PPOAgent
from tensorforce.execution import Runner
from tensorforce.contrib.openai_gym import OpenAIGym

# Create an OpenAIgym environment.
environment = OpenAIGym('CartPole-v0', visualize=True)
network_spec = [
    dict(type='dense', size=32, activation='relu'),
    dict(type='dense', size=32, activation='relu')
]
agent = PPOAgent(
    states=environment.states,
    actions=environment.actions,
    network=network_spec,
    step_optimizer=dict(
        type='adam',
        learning_rate=1e-3
    ),
    saver=dict(directory='./saver/', basename='PPO_model.ckpt', load=False, seconds=600),
    summarizer=dict(directory='./record/', labels=["losses", "entropy"], seconds=600),
)
# Create the runner
runner = Runner(agent=agent, environment=environment)
# Start learning
runner.run(episodes=600, max_episode_timesteps=200)
runner.close()

if __name__ == "__main__":
    pass
