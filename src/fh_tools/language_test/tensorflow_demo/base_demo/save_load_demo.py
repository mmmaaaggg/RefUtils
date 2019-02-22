#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2019/02/22 上午9:54
@File    : save_load_demo.py
@contact : mmmaaaggg@163.com
@desc    : 
"""
import tensorflow as tf


## save to file
W = tf.Variable([[1, 2, 3], [3, 4, 5]], dtype=tf.float32, name="weights")
b = tf.Variable([[1, 2, 3]], dtype=tf.float32, name="biases")

init = tf.global_variables_initializer()

saver = tf.train.Saver()

with tf.Session() as sess:
    sess.run(init)
    save_path = saver.save(sess, r"my_net/save_net.ckpt")
    print("Save to path:", save_path)

