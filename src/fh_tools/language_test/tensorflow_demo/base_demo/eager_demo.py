#! /usr/bin/env python3
"""
@author  : MG
@Time    : 2020/2/5 上午8:58
@File    : eager_demo.py
@contact : mmmaaaggg@163.com
@desc    : 
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import os
import tensorflow as tf

import cProfile

# In Tensorflow 2.0, eager execution is enabled by default.
tf.executing_eagerly()
x = [[2.]]
m = tf.matmul(x, x)
print("hello, {}".format(m))

a = tf.constant([[1, 2],
                 [3, 4]])
print(a)

if __name__ == "__main__":
    pass
