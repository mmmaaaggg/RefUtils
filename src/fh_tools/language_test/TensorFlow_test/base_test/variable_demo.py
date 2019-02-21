#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2019/02/20 下午5:17
@File    : variable_demo
@contact : mmmaaaggg@163.com
@desc    : tf.Variable
"""
import tensorflow as tf

state = tf.Variable(0, name="counter")
# print(state)
one = tf.constant(1)
new_value = tf.add(state, one)
update = tf.assign(state, new_value)

init = tf.initialize_all_variables()  # must have if define variable

with tf.Session() as sess:
    sess.run(init)
    for _ in range(3):
        sess.run(update)
        print(sess.run(state))


