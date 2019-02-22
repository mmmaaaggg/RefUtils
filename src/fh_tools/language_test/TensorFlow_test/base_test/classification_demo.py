#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2019/02/21 下午2:46
@File    : classification_demo.py
@contact : mmmaaaggg@163.com
@desc    : 
"""
import tensorflow as tf
import tensorflow.examples.tutorials.mnist.input_data as input_data

mnist = input_data.read_data_sets('MNIST_data', one_hot=True)


def add_layer(input, in_size, out_size, n_layer, activation_function=None):
    layer_name = f"layer{n_layer}"
    with tf.name_scope(layer_name):
        with tf.name_scope("weights"):
            Weights = tf.Variable(tf.random_normal([in_size, out_size]))
            tf.summary.histogram(layer_name + "/weights", Weights)
        with tf.name_scope("biases"):
            biases = tf.Variable(tf.zeros([1, out_size]) + 0.1)
            tf.summary.histogram(layer_name + "/biases", biases)
        with tf.name_scope("Wx_plus_b"):
            Wx_plus_b = tf.matmul(input, Weights) + biases

        if activation_function is None:
            outputs = Wx_plus_b
        else:
            outputs = activation_function(Wx_plus_b)

        tf.summary.histogram(layer_name + "/outputs", outputs)
        return outputs


xs = tf.placeholder(tf.float32, [None, 784])  # 28 * 28 = 784
ys = tf.placeholder(tf.float32, [None, 10])

# add output layer
prediction = add_layer(xs, 784, 10, n_layer=1, activation_function=tf.nn.softmax)

# the error between prediction and real data
cross_entropy = tf.reduce_mean(
    -tf.reduce_sum(ys * tf.log(prediction),
                   reduction_indices=[1]))  # loss

train_setp = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)


def compute_accuracy(sess, v_xs, v_ys):
    global prediction
    y_pre = sess.run(prediction, feed_dict={xs: v_xs})
    correct_prediction = tf.equal(tf.argmax(y_pre, 1), tf.argmax(v_ys, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    result = sess.run(accuracy, feed_dict={xs: batch_xs, ys: batch_ys})
    return result


with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for i in range(1000):
        batch_xs, batch_ys = mnist.train.next_batch(100)
        sess.run(train_setp, feed_dict={xs: batch_xs, ys: batch_ys})
        if i % 50 == 0:
            print(compute_accuracy(
                sess, mnist.test.images, mnist.test.labels
            ))

