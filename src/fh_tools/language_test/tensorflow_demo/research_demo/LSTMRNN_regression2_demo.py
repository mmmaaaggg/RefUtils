#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2019/2/28 15:46
@File    : LSTMRNN_regression_demo.py
@contact : mmmaaaggg@163.com
@desc    : 利用 RNN LSTM 进行回归分析，预测下一步曲线
"""
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from fh_tools.quant import get_target_by_future_pct_range

BATCH_START = 0
TIME_STEPS = 20
BATCH_SIZE = 50
INPUT_SIZE = 2
OUTPUT_SIZE = 1
CELL_SIZE = 10
LR = 0.006
BATCH_START_TEST = 0


def get_batch(show_plt=False):
    """
    够在一系列输入输出数据集
    target： 目标是一条cos曲线
    res： 两条同频率，不同位移的sin曲线
    xs：X 序列
    """
    global BATCH_START, TIME_STEPS
    # xs shape(50 batch, 20 steps)
    xs = np.arange(BATCH_START, BATCH_START + TIME_STEPS * BATCH_SIZE).reshape((BATCH_SIZE, TIME_STEPS))
    inputs = np.zeros((BATCH_SIZE, TIME_STEPS, 2))
    inputs[:, :, 0] = xs
    inputs[:, :, 1] = xs - 0.5
    # seq = np.zeros((BATCH_SIZE, TIME_STEPS, 2))
    # seq[:, :, 0] = np.sin(xs)
    # seq[:, :, 1] = np.sin(xs - 0.5)
    target = np.sin(inputs) + 5
    target = get_target_by_future_pct_range(target, -0.1, 0.1)
    res = np.cos(xs)
    BATCH_START += TIME_STEPS
    if show_plt:
        plt.plot(xs[0, :], res[0, :], 'r',
                 xs[0, :], target[0, :, 0], 'b--',
                 xs[0, :], target[0, :, 1], 'b')
        plt.show()
    # returned seq, res and shape (batch, step, input)
    return target, res[:, :, np.newaxis], xs


class LSTMRNN:
    def __init__(self, n_step, input_size, output_size, cell_size, batch_size):
        self.n_step = n_step
        self.input_size = input_size
        self.output_size = output_size
        self.cell_size = cell_size
        self.batch_size = batch_size
        self.cost = None
        self.l_in_y = None
        self.cell_outputs = None
        self.cell_init_state = None
        self.cell_final_state = None
        with tf.name_scope('inputs'):
            self.xs = tf.placeholder(tf.float32, [None, n_step, input_size], name='xs')
            self.ys = tf.placeholder(tf.float32, [None, n_step, output_size], name='ys')

        with tf.variable_scope('in_hidden'):
            self.add_input_layer()
        with tf.variable_scope('LSTM_cell'):
            self.add_cell()
        with tf.variable_scope('out_hidden'):
            self.add_output_layer()
        with tf.name_scope('cost'):
            self.compute_cost()
        with tf.name_scope('train'):
            self.train_op = tf.train.AdamOptimizer(LR).minimize(self.cost)

    def add_input_layer(self):
        l_in_x = tf.reshape(self.xs, [-1, self.input_size], name='2_2D')  # (batch*n_step, in_size)
        # Ws(in_size, cell_size)
        Ws_in = self._weight_variable([self.input_size, self.cell_size])
        # bs(cell_size, )
        bs_in = self._bias_variable([self.cell_size, ])
        # l_in_y = (batch * n_steps, cell_size)
        with tf.name_scope('Wx_plus_b'):
            l_in_y = tf.matmul(l_in_x, Ws_in) + bs_in
        # reshape l_in_y ==> (batch, n_steps, cell_size)
        self.l_in_y = tf.reshape(l_in_y, [-1, self.n_step, self.cell_size], name='2_3D')

    def add_cell(self):
        lstm_cell = tf.nn.rnn_cell.BasicLSTMCell(self.cell_size, forget_bias=1.0, state_is_tuple=True)
        with tf.name_scope('initial_state'):
            self.cell_init_state = lstm_cell.zero_state(self.batch_size, dtype=tf.float32)
        self.cell_outputs, self.cell_final_state = tf.nn.dynamic_rnn(
            lstm_cell, self.l_in_y, initial_state=self.cell_init_state, time_major=False
        )

    def add_output_layer(self):
        # shape = (batch * steps, cell_size)
        l_out_x = tf.reshape(self.cell_outputs, [-1, self.cell_size], name='2_2D')  # (batch*n_step, in_size)
        # Ws(in_size, cell_size)
        Ws_out = self._weight_variable([self.cell_size, self.output_size])
        # bs(output_size, )
        bs_out = self._bias_variable([self.output_size, ])
        # shape = (batch * n_steps, output_size)
        with tf.name_scope('Wx_plus_b'):
            self.pred = tf.matmul(l_out_x, Ws_out) + bs_out

    def compute_cost(self):
        losses = tf.contrib.legacy_seq2seq.sequence_loss_by_example(
            [tf.reshape(self.pred, [-1], name='reshape_pred')],
            [tf.reshape(self.ys, [-1], name='reshape_target')],
            [tf.ones([self.batch_size * self.n_step], dtype=tf.float32)],
            average_across_timesteps=True,
            softmax_loss_function=self.msr_error,
            name='losses'
        )

        with tf.name_scope('average_cost'):
            self.cost = tf.div(
                tf.reduce_sum(losses, name='losses_sum'),
                tf.cast(self.batch_size, tf.float32),
                name='average_cost'
            )
            tf.summary.scalar('cost', self.cost)

    def msr_error(self, logits, labels):
        return tf.square(tf.subtract(logits, labels))  # tf.sub(..., ...)

    def _weight_variable(self, shape, name='weights'):
        initializer = tf.random_normal_initializer(mean=0., stddev=1.)
        return tf.get_variable(shape=shape, initializer=initializer, name=name)

    def _bias_variable(self, shape, name='biases'):
        initializer = tf.constant_initializer(0.1)
        return tf.get_variable(shape=shape, initializer=initializer, name=name)


def train(plot_batch_or_ion="batch"):
    model = LSTMRNN(TIME_STEPS, INPUT_SIZE, OUTPUT_SIZE, CELL_SIZE, BATCH_SIZE)
    with tf.Session() as sess:
        merged = tf.summary.merge_all()
        writer = tf.summary.FileWriter('logs', sess.graph)
        # relocate to the local dir and run this line to view it on Chrome(http://0.0.0.0:6006/):
        # $ tensorboard --logdir='logs'

        sess.run(tf.global_variables_initializer())
        if plot_batch_or_ion == 'ion':
            plt.ion()
            plt.show()

        batch_start, xs_batch, res_batch, pred_batch = BATCH_START, None, None, None
        for i in range(200):
            seq, res, xs = get_batch()
            if i == 0:
                feed_dict = {
                    model.xs: seq,
                    model.ys: res,
                    # create initial state
                }
            else:
                feed_dict = {
                    model.xs: seq,
                    model.ys: res,
                    model.cell_init_state: state,  # use last state as the initial state for this run
                }

            _, cost, state, pred = sess.run(
                [model.train_op, model.cost, model.cell_final_state, model.pred],
                feed_dict=feed_dict
            )

            # plotting
            if plot_batch_or_ion == 'ion':
                plt.plot(xs[0, :], res[0].flatten(), 'r', xs[0, :], pred.flatten()[:TIME_STEPS], 'b--')
                plt.ylim((-1.2, 1.2))
                plt.draw()
                plt.pause(0.3)
            elif plot_batch_or_ion == 'batch':
                if xs_batch is None:
                    xs_batch = xs[0, :]
                    res_batch = res[0].flatten()
                    pred_batch = pred.flatten()[:TIME_STEPS]
                else:
                    xs_batch = np.append(xs_batch, xs[0, :])
                    res_batch = np.append(res_batch, res[0].flatten())
                    pred_batch = np.append(pred_batch, pred.flatten()[:TIME_STEPS])

            if i % 20 == 0:
                print('cost:', round(cost, 4))
                result = sess.run(merged, feed_dict)
                writer.add_summary(result, i)
                if plot_batch_or_ion == 'batch':
                    # default is (6.4, 4.8) for size 640*480 pix
                    plt.figure(figsize=(40.96, 8))
                    plt.subplots_adjust(hspace=0.2, wspace=0.2)
                    plt.plot(xs_batch, res_batch, 'r', xs_batch, pred_batch, 'b--', linewidth=1)
                    plt.ylim((-1.2, 1.2))
                    plt.xlim((min(xs_batch), max(xs_batch)))
                    plt.show()
                    batch_start, xs_batch, res_batch, pred_batch = BATCH_START, None, None, None


if __name__ == "__main__":
    get_batch(show_plt=True)

    train()
