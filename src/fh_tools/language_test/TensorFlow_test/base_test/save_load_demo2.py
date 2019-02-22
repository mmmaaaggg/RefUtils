#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2019/02/22 上午9:59
@File    : save_load_demo2.py
@contact : mmmaaaggg@163.com
@desc    : 
"""
import tensorflow as tf
import numpy as np

# restore variables
# redefine the same shape and same type for your variables
W = tf.Variable(np.arange(6).reshape((2, 3)), dtype=tf.float32, name="weights")
b = tf.Variable(np.arange(3).reshape((1, 3)), dtype=tf.float32, name="biases")

# not need init step

saver = tf.train.Saver()
with tf.Session() as sess:
    saver.restore(sess, r"my_net/save_net.ckpt")
    print("weights:", sess.run(W))
    print("biases:", sess.run(b))

