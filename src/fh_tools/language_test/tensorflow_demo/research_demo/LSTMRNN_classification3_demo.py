#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2019/03/19 16:09
@File    : LSTMRNN_classification3_demo.py
@contact : mmmaaaggg@163.com
@desc    : 期货连续合约量价数据，输出前复权价格未来波动是否可能超过 -1%或 1%
根据一组输入（双sin曲线+cos曲线），将其按移动窗口分割成 batch_size 大小的训练集
"""
import tensorflow as tf
import numpy as np
# from tensorflow.examples.tutorials.mnist import input_data
import matplotlib.pyplot as plt
from src.fh_tools.fh_utils import get_last_idx
import pandas as pd

# mnist = input_data.read_data_sets("MNIST_data", one_hot=True)
BATCH_START = 0
TIME_STEPS = 20
BATCH_SIZE = 50
INPUT_SIZE = 3
OUTPUT_SIZE = 2
CELL_SIZE = 10
LR = 0.006
BATCH_START_TEST = 0


def get_factors():
    global INPUT_SIZE
    # '/home/mg/github/RefUtils/src/fh_tools/language_test/tensorflow_demo/research_demo/RU_continuous_adj.csv'
    file_path = r'RU_continuous_adj.csv'
    df = pd.read_csv(file_path, index_col=0)
    df = df[~df['close'].isnull()][['close', 'TermStructure', 'Volume', 'OI']]

    factors = df.to_numpy()
    price_arr = factors[:, 0]
    INPUT_SIZE = factors.shape[1]
    labels = get_label_by_future_value(price_arr, -0.01, 0.01)
    idx_last_available_label = get_last_idx(labels, lambda x: x.sum() == 0)
    factors = factors[:idx_last_available_label + 1, :]
    labels = labels[:idx_last_available_label + 1, :]
    return factors, labels


def get_label_by_future_value(value_arr: np.ndarray, min_pct: float, max_pct: float, max_future=None):
    """
    根据时间序列数据 pct_arr 计算每一个时点目标标示 -1 0 1
    计算方式：当某一点未来波动首先 >（ 或 <） 上届 min_pct（或下届 max_pct），则标记为 1 （或 -1）
    :param value_arr:
    :param min_pct:
    :param max_pct:
    :param max_future:最大搜索长度
    :return:
    """
    value_arr[np.isnan(value_arr)] = 0
    arr_len = value_arr.shape[0]
    target_arr = np.zeros((arr_len, OUTPUT_SIZE))
    for i in range(arr_len):
        base = value_arr[i]
        for j in range(i+1, arr_len):
            result = value_arr[j] / base - 1
            if result < min_pct:
                target_arr[i, 0] = 1
                break
            elif result > max_pct:
                target_arr[i, 1] = 1
                break
    return target_arr


def get_batch(factors: np.ndarray, labels: np.ndarray, shift=2, show_plt=False):
    """
    够在一系列输入输出数据集
    xs： 两条同频率，不同位移的sin曲线
    ys_value： 目标是一条cos曲线
    ys: ys_value 未来涨跌标识
    i_s：X 序列
    """
    global BATCH_START, TIME_STEPS

    xs = np.zeros((BATCH_SIZE, TIME_STEPS, INPUT_SIZE))
    ys = np.zeros((BATCH_SIZE, OUTPUT_SIZE))
    available_batch_size, num = 0, 0
    print(f"range({BATCH_START}, {factors.shape[0]}, {shift})")
    for available_batch_size, num in enumerate(range(BATCH_START, factors.shape[0], shift)):
        tmp = factors[num:num + TIME_STEPS, :]
        if tmp.shape[0] < TIME_STEPS:
            break
        xs[available_batch_size, :, :] = tmp
        ys[available_batch_size, :] = labels[num + TIME_STEPS - 1, :]
        if available_batch_size + 1 >= BATCH_SIZE:
            available_batch_size += 1
            break

    # i_s shape(50 batch, 20 steps)
    BATCH_START = num + shift
    if show_plt:
        xx = list(range(TIME_STEPS))
        plt.plot(xx, xs[0, :, 0], 'b--',
                 xx, xs[0, :, 1], 'b',
                 xx, xs[0, :, 2], 'r',
                 # xx, ys, 'r--',
                 )
        plt.show()
    # returned xs, ys_value and shape (batch, step, input)
    return xs, ys, available_batch_size


class LSTMRNN:
    def __init__(self, n_step, n_inputs, n_hidden_units, n_classes, lr, batch_size):
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
        self.batch_size = batch_size
        # attributes defined in other functions
        self.cost = None
        self.l_in_y = None
        self.cell_outputs = None
        self.cell_init_state = None
        self.cell_final_state = None

        with tf.name_scope('inputs'):
            # tf Graph input
            self.xs = tf.placeholder(tf.float32, [None, n_step, n_inputs])
            self.ys = tf.placeholder(tf.float32, [None, n_classes])

        # Define weights
        self.weights = {
            # 28*128
            'in': tf.Variable(tf.random_normal([n_inputs, n_hidden_units])),
            # (128, 10)
            'out': tf.Variable(tf.random_normal([n_hidden_units, n_classes]))
        }

        self.biases = {
            # (128, )
            'in': tf.Variable(tf.constant(0.1, shape=[n_hidden_units, ])),
            # (10, )
            'out': tf.Variable(tf.constant(0.1, shape=[n_classes, ]))
        }
        with tf.variable_scope('in_hidden'):
            self.add_input_layer()
        with tf.variable_scope('LSTM_cell'):
            self.add_cell()
        with tf.variable_scope('out_hidden'):
            self.add_output_layer()
        with tf.name_scope('cost'):
            self.compute_cost()
        with tf.name_scope('train'):
            self.train_op = tf.train.AdamOptimizer(self.lr).minimize(self.cost)
        with tf.name_scope('accuracy'):
            correct_pred = tf.equal(tf.argmax(self.pred, 1), tf.argmax(self.ys, 1))
            self.accuracy_op = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

    def add_input_layer(self):
        # hidden layer for input to cell
        # X (128 batch, 28 steps, 28 inputs)
        # ==> X (128 * 28, 28 inputs)
        l_in_x = tf.reshape(self.xs, [-1, self.n_inputs])
        Ws_in = tf.Variable(tf.random_normal([self.n_inputs, self.n_hidden_units]))
        bs_in = tf.Variable(tf.constant(0.1, shape=[self.n_hidden_units, ]))
        # ==> X_in (128 batch * 28 steps, 128 hidden)
        with tf.name_scope('Wx_plus_b'):
            l_in_y = tf.matmul(l_in_x, Ws_in) + bs_in
        # ==> X_in (128 batch, 28 steps, 128 hidden)
        self.l_in_y = tf.reshape(l_in_y, [-1, self.n_step, self.n_hidden_units])

    def add_cell(self):
        # cell
        lstm_cell = tf.nn.rnn_cell.BasicLSTMCell(self.n_hidden_units, forget_bias=1.0, state_is_tuple=True)
        with tf.name_scope('initial_state'):
            # lstm cell is divided into two parts (c_state, m_state)
            self.cell_init_state = lstm_cell.zero_state(self.batch_size, dtype=tf.float32)

        self.cell_outputs, self.cell_final_state = tf.nn.dynamic_rnn(lstm_cell, self.l_in_y, initial_state=self.cell_init_state, time_major=False)

    def add_output_layer(self):
        # hidden layer for output as the final results
        # method 1
        # results = tf.matmul(states[1], weights['out']) + biases['out']  # states[1] is m_state
        # method 2
        # unpack to list[(batch, outputs)...] * steps
        l_out_x = tf.unstack(tf.transpose(self.cell_outputs, [1, 0, 2]))  # states is the last outputs
        Ws_out = tf.Variable(tf.random_normal([self.n_hidden_units, self.n_classes]))
        bs_out = tf.Variable(tf.constant(0.1, shape=[self.n_classes, ]))
        self.pred = tf.matmul(l_out_x[-1], Ws_out) + bs_out

    def compute_cost(self):
        self.cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(
            logits=self.pred, labels=self.ys))
        tf.summary.scalar('cost', self.cost)


def train():
    factors, labels = get_factors()
    # hyperparameters
    lr = LR
    training_iters = 100000
    batch_size = BATCH_SIZE

    n_inputs = INPUT_SIZE  # MNIST data input (img shape 28*28)
    n_step = TIME_STEPS  # time steps
    n_hidden_units = CELL_SIZE  # neurons in hidden layer
    n_classes = OUTPUT_SIZE  # MNIST classes (0-9 digits)
    model = LSTMRNN(n_step, n_inputs, n_hidden_units, n_classes, lr, batch_size)
    with tf.Session() as sess:
        merged = tf.summary.merge_all()
        writer = tf.summary.FileWriter('logs', sess.graph)
        # relocate to the local dir and run this line to view it on Chrome(http://0.0.0.0:6006/):
        # $ tensorboard --logdir='logs'

        sess.run(tf.global_variables_initializer())
        step = 0
        while step * model.batch_size < training_iters:
            # batch_xs, batch_ys = mnist.train.next_batch(model.batch_size)
            # batch_xs.shape, batch_ys.shape
            batch_xs, batch_ys, available_batch_size = get_batch(factors, labels)
            # print("available_batch_size", available_batch_size)
            if available_batch_size < model.batch_size:
                break
            # batch_xs = batch_xs.reshape([model.batch_size, model.n_step, model.n_inputs])
            # feed_dict = {model.xs: batch_xs, model.ys: batch_ys}
            # sess.run(model.train_op, feed_dict=feed_dict)
            if step == 0:
                feed_dict = {
                    model.xs: batch_xs,
                    model.ys: batch_ys,
                    # create initial state
                }
            else:
                feed_dict = {
                    model.xs: batch_xs,
                    model.ys: batch_ys,
                    model.cell_init_state: state,  # use last state as the initial state for this run
                }

            # sess.run(model.train_op, feed_dict=feed_dict)
            _, cost, state, pred = sess.run(
                [model.train_op, model.cost, model.cell_final_state, model.pred]
                , feed_dict=feed_dict
            )

            if step % 20 == 0:
                # batch_xs, batch_ys, _ = get_batch(factors, labels)
                # if step == 0:
                #     feed_dict = {
                #         model.xs: batch_xs,
                #         model.ys: batch_ys,
                #         # create initial state
                #     }
                # else:
                #     feed_dict = {
                #         model.xs: batch_xs,
                #         model.ys: batch_ys,
                #         model.cell_init_state: state,  # use last state as the initial state for this run
                #     }
                print(sess.run(model.accuracy_op, feed_dict=feed_dict))
                result = sess.run(merged, feed_dict)
                writer.add_summary(result, step)

            step += 1


if __name__ == '__main__':
    train()
