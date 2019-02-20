#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 19-2-20 下午8:54
@File    : placeholder_demo
@contact : mmmaaaggg@163.com
@desc    :  
"""
import tensorflow as tf

input1 = tf.placeholder(tf.float32)
input2 = tf.placeholder(tf.float32)

output = tf.multiply(input1, input2)

with tf.Session() as sess:
    print(sess.run(output, feed_dict={
        input1: [7.],
        input2: [2.]
    }))
