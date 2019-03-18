#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2019/02/22 上午10:09
@File    : rnn_classification_demo.py
@contact : mmmaaaggg@163.com
@desc    : 
"""
import tensorflow as tf
import numpy as np
from tensorflow.examples.tutorials.mnist import input_data

mnist = input_data.read_data_sets("MNIST_data", one_hot=True)


class LSTMRNN:
    def __init__(self, n_step, n_inputs, n_hidden_units, n_classes, lr, training_iters, batch_size):
        """

        :param n_step: time steps
        :param n_inputs: MNIST data input (img shape 28*28)
        :param n_hidden_units: neurons in hidden layer
        :param n_classes: MNIST classes (0-9 digits)
        :param lr:
        :param training_iters:
        :param batch_size:
        """
        self.n_step = n_step
        self.n_inputs = n_inputs
        self.n_hidden_units = n_hidden_units
        self.n_classes = n_classes
        # hyperparameters
        self.lr = lr
        self.training_iters = training_iters
        self.batch_size = batch_size
        self.batch_size = batch_size
        self.batch_size = batch_size
        self.batch_size = batch_size
        self.batch_size = batch_size
        self.batch_size = batch_size

        with tf.name_scope('inputs'):
            # tf Graph input
            self.xs = tf.placeholder(tf.float32, [None, n_step, n_inputs])
            self.ys = tf.placeholder(tf.float32, [None, n_classes])

        # Define weights
        weights = {
            # 28*128
            'in': tf.Variable(tf.random_normal([n_inputs, n_hidden_units])),
            # (128, 10)
            'out': tf.Variable(tf.random_normal([n_hidden_units, n_classes]))
        }

        biases = {
            # (128, )
            'in': tf.Variable(tf.constant(0.1, shape=[n_hidden_units, ])),
            # (10, )
            'out': tf.Variable(tf.constant(0.1, shape=[n_classes, ]))
        }
        with tf.variable_scope('in_hidden'):
            self.add_input_layer()

    def add_input_layer(self):
        # hidden layer for input to cell
        # X (128, batch, 28 steps, 28 inputs)
        # ==> X (128 * 28, 28 inputs)
        l_in_x = tf.reshape(self.xs, [-1, self.n_inputs])
        Ws_in = tf.Variable(tf.random_normal([n_inputs, n_hidden_units]))
        bs_in = tf.Variable(tf.constant(0.1, shape=[n_hidden_units, ]))
        # ==> X_in (128 batch * 28 steps, 128 hidden)
        with tf.name_scope('Wx_plus_b'):
            l_in_y = tf.matmul(l_in_x, Ws_in) + bs_in
        # ==> X_in (128 batch, 28 steps, 128 hidden)
        X_in = tf.reshape(X_in, [-1, n_step, n_hidden_units])


# hyperparameters
lr = 0.001
training_iters = 100000
batch_size = 128

n_inputs = 28           # MNIST data input (img shape 28*28)
n_step = 28            # time steps
n_hidden_units = 128     # neurons in hidden layer
n_classes = 10          # MNIST classes (0-9 digits)

# tf Graph input
x = tf.placeholder(tf.float32, [None, n_step, n_inputs])
y = tf.placeholder(tf.float32, [None, n_classes])

# Define weights
weights = {
    # 28*128
    'in': tf.Variable(tf.random_normal([n_inputs, n_hidden_units])),
    # (128, 10)
    'out': tf.Variable(tf.random_normal([n_hidden_units, n_classes]))
}

biases = {
    # (128, )
    'in': tf.Variable(tf.constant(0.1, shape=[n_hidden_units, ])),
    # (10, )
    'out': tf.Variable(tf.constant(0.1, shape=[n_classes, ]))
}


def RNN(X, weights, biases):
    # hidden layer for input to cell
    # X (128, batch, 28 steps, 28 inputs)
    # ==> X (128 * 28, 28 inputs)
    X = tf.reshape(X, [-1, n_inputs])
    # ==> X_in (128 batch * 28 steps, 128 hidden)
    X_in = tf.matmul(X, weights['in']) + biases['in']
    # ==> X_in (128 batch, 28 steps, 128 hidden)
    X_in = tf.reshape(X_in, [-1, n_step, n_hidden_units])

    # cell
    lstm_cell = tf.nn.rnn_cell.BasicLSTMCell(n_hidden_units, forget_bias=1.0, state_is_tuple=True)
    # lstm cell is divided into two parts (c_state, m_state)
    _init_state = lstm_cell.zero_state(batch_size, dtype=tf.float32)

    outputs, states = tf.nn.dynamic_rnn(lstm_cell, X_in, initial_state=_init_state, time_major=False)

    # hidden layer for output as the final results
    # method 1
    # results = tf.matmul(states[1], weights['out']) + biases['out']  # states[1] is m_state
    # method 2
    # unpack to list[(batch, outputs)...] * steps
    outputs = tf.unstack(tf.transpose(outputs, [1, 0, 2]))  # states is the last outputs
    results = tf.matmul(outputs[-1], weights['out']) + biases['out']

    return results


pred = RNN(x, weights, biases)
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=pred, labels=y))
train_op = tf.train.AdamOptimizer(lr).minimize(cost)

correct_pred = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

init = tf.global_variables_initializer()
with tf.Session() as sess:
    sess.run(init)
    step = 0
    while step * batch_size < training_iters:
        batch_xs, batch_ys = mnist.train.next_batch(batch_size)
        batch_xs = batch_xs.reshape([batch_size, n_step, n_inputs])
        sess.run(train_op, feed_dict={x: batch_xs, y: batch_ys})

        if step % 20 == 0:
            print(sess.run(accuracy, feed_dict={
                x: batch_xs,
                y: batch_ys
            }))

        step += 1
