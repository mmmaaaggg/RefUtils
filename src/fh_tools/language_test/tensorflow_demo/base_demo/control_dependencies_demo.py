#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 19-4-2 下午4:50
@File    : control_dependencies_demo.py
@contact : mmmaaaggg@163.com
@desc    : 
"""
import tensorflow as tf

g = tf.Graph()
with g.as_default():
    x = tf.Variable(1.0, name='x')
    x_plus_1 = tf.assign_add(x, 1, name='x_plus')

    with tf.control_dependencies([x_plus_1]):
        y = x
        z = tf.identity(x, name='z_added')

    init = tf.global_variables_initializer()

    with tf.Session() as sess:
        sess.run(init)
        for i in range(5):
            print(sess.run(z))
            # 输出 2,3,4,5,6
            # print(sess.run(y))
            # 如果改为输出 print(sess.run(y)) ,则结果为 1,1,1,1,1
