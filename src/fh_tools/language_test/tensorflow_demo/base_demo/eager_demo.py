#! /usr/bin/env python3
"""
@author  : MG
@Time    : 2020/2/5 上午8:58
@File    : eager_demo.py
@contact : mmmaaaggg@163.com
@desc    : 
"""
from __future__ import absolute_import, division, print_function
import tensorflow as tf
# tensorflow 2.0 开始 tensorflow.contrib 被放弃
import tensorflow.contrib.eager as tfe

tfe.enable_eager_execution()

x = [[2.]]
m = tf.matmul(x, x)
print("hello, {}".format(m))  # => "hello, [[4.]]"

if __name__ == "__main__":
    pass
