#! /usr/bin/env python3
"""
@author  : MG
@Time    : 2020/2/7 下午5:35
@File    : replay_buffer_demo.py
@contact : mmmaaaggg@163.com
@desc    : 
"""
# from __future__ import absolute_import
# from __future__ import division
# from __future__ import print_function
import numpy as np
import tensorflow as tf
from tensorflow_core.python.framework.errors_impl import InvalidArgumentError
from tf_agents.replay_buffers.tf_uniform_replay_buffer import TFUniformReplayBuffer
from tf_agents.specs import tensor_spec

# tf.compat.v1.enable_v2_behavior()

data_spec = (
    tf.TensorSpec([3], tf.float32, 'action'),
    (
        tf.TensorSpec([5], tf.float32, 'lidar'),
        tf.TensorSpec([3, 2], tf.float32, 'camera')
    )
)
batch_size = 32
max_length = 1000

replay_buffer = TFUniformReplayBuffer(data_spec=data_spec, batch_size=batch_size, max_length=max_length)

action = tf.constant(1 * np.ones(data_spec[0].shape.as_list(), dtype=np.float32))
lidar = tf.constant(2 * np.ones(data_spec[1][0].shape.as_list(), dtype=np.float32))
camera = tf.constant(3 * np.ones(data_spec[1][1].shape.as_list(), dtype=np.float32))

values = (action, (lidar, camera))
values_batched = tf.nest.map_structure(lambda t: tf.stack([t] * batch_size), values)
for _ in range(5):
    replay_buffer.add_batch(values_batched)

sample = replay_buffer.get_next(sample_batch_size=10, num_steps=2)

dataset = replay_buffer.as_dataset(sample_batch_size=4, num_steps=1)
iterator = iter(dataset)
print("Iterator trajectories:")
trajectories = []
for _ in range(3):
    t, _ = next(iterator)
    trajectories.append(t)

print(tf.nest.map_structure(lambda t: t.shape, trajectories))

replay_buffer.gather_all()

if __name__ == "__main__":
    pass
