# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 15:59:03 2017

@author: forise
"""

import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import pandas as pd
from src.fh_tools.language_test.TensorFlow_test.config_fh import get_db_engine
from tensorflow.python.platform import tf_logging as logging


def ln(tensor, scope=None, epsilon=1e-5):
    """ Layer normalizes a 2D tensor along its second axis """
    assert (len(tensor.get_shape()) == 2)
    m, v = tf.nn.moments(tensor, [1], keep_dims=True)
    if not isinstance(scope, str):
        scope = ''
    with tf.variable_scope(scope + 'layer_norm'):
        scale = tf.get_variable('scale',
                                shape=[tensor.get_shape()[1]],
                                initializer=tf.constant_initializer(1))
        shift = tf.get_variable('shift',
                                shape=[tensor.get_shape()[1]],
                                initializer=tf.constant_initializer(0))
    LN_initial = (tensor - m) / tf.sqrt(v + epsilon)

    return LN_initial * scale + shift


class Q_BasicLSTMCell_with_normalize(tf.contrib.rnn.RNNCell):
    def __init__(self, num_units, forget_bias=1.0, input_size=None,
                 state_is_tuple=True, activation=tf.tanh):
        if not state_is_tuple:
            logging.warn("%s: Using a concatenated state is slower and will soon be "
                         "deprecated.  Use state_is_tuple=True.", self)
        if input_size is not None:
            logging.warn("%s: The input_size parameter is deprecated.", self)
        self._num_units = num_units
        self._forget_bias = forget_bias
        self._state_is_tuple = state_is_tuple
        self._activation = activation

    @property
    def state_size(self):
        return (tf.contrib.rnn.LSTMStateTuple(self._num_units, self._num_units)
                if self._state_is_tuple else 2 * self._num_units)

    @property
    def output_size(self):
        return self._num_units

    def __call__(self, inputs, state, scope=None):
        """Long short-term memory cell (LSTM)."""
        from tensorflow.python.ops import array_ops
        from tensorflow.contrib.rnn.python.ops.core_rnn_cell_impl import _linear as linear
        with tf.variable_scope(scope or "basic_lstm_cell"):
            # Parameters of gates are concatenated into one multiply for efficiency.
            if self._state_is_tuple:
                c, h = state
            else:
                c, h = array_ops.split(value=state, num_or_size_splits=2, axis=1)
            concat = linear([inputs, h], 4 * self._num_units, True, scope=scope)

            # i = input_gate, j = new_input, f = forget_gate, o = output_gate
            i, j, f, o = array_ops.split(value=concat, num_or_size_splits=4, axis=1)
            i = ln(i, scope='i/')
            j = ln(i, scope='j/')
            f = ln(i, scope='f/')
            o = ln(i, scope='o/')

            new_c = (c * tf.sigmoid(f + self._forget_bias) + tf.sigmoid(i) *
                     self._activation(j))
            new_h = self._activation(new_c) * tf.sigmoid(o)

            if self._state_is_tuple:
                new_state = tf.contrib.rnn.LSTMStateTuple(new_c, new_h)
            else:
                new_state = array_ops.concat([new_c, new_h], 1)
            return new_h, new_state


def gen_batchND(raw_data, batch_size, num_steps):
    p_features = raw_data.shape[1] - 1
    ColNames = raw_data.columns
    raw_y = np.array(raw_data[ColNames[p_features]])
    data_length = len(raw_y)

    # partition raw data into batches and stack them vertically in a data matrix
    batch_partition_length = data_length // batch_size
    epoch_size = batch_partition_length // num_steps

    #    data_x = np.zeros([batch_size, batch_partition_length], dtype=np.int32)
    data_x = np.zeros([p_features, batch_size, batch_partition_length])
    data_y = np.zeros([batch_size, batch_partition_length], dtype=np.int32)
    for i in range(batch_size):
        data_y[i] = raw_y[batch_partition_length * i:batch_partition_length * (i + 1)]
    for p in range(p_features):
        raw_x = np.array(raw_data[ColNames[p]])
        for i in range(batch_size):
            data_x[p][i] = raw_x[batch_partition_length * i:batch_partition_length * (i + 1)]
    # further divide batch partitions into num_steps for truncated backprop

    for i in range(epoch_size):
        x = data_x[:, :, i * num_steps:(i + 1) * num_steps]
        y = data_y[:, i * num_steps:(i + 1) * num_steps]
        yield (x, y)


def variable_summaries(var):
    """Attach a lot of summaries to a Tensor (for TensorBoard visualization)."""
    var = tf.cast(var, tf.float32)
    with tf.name_scope('summaries'):
        mean = tf.reduce_mean(var)
        tf.summary.scalar('mean', mean)
        with tf.name_scope('stddev'):
            stddev = tf.sqrt(tf.reduce_mean(tf.square(var - mean)))
        tf.summary.scalar('stddev', stddev)
        tf.summary.scalar('max', tf.reduce_max(var))
        tf.summary.scalar('min', tf.reduce_min(var))
        tf.summary.histogram('histogram', var)


def reset_graph():
    if 'sess' in globals() and sess:
        sess.close()
    tf.reset_default_graph()


def build_graph(
        num_steps,  # number of truncated backprop steps
        batch_size,
        num_classes,
        state_size,
        learning_rate,
        p_num,
        num_layers,
):
    tf.summary.scalar('num_layers', num_layers)

    reset_graph()
    with tf.name_scope('input'):
        x = tf.placeholder(tf.float32, [p_num, batch_size, num_steps], name='input_placeholder')
        y = tf.placeholder(tf.int32, [batch_size, num_steps], name='labels_placeholder')
        variable_summaries(x)
        variable_summaries(y)
    with tf.name_scope('reshape_input'):
        y_as_list = tf.unstack(y, num=num_steps, axis=1)
    with tf.name_scope('pre-process'):
        rnn_inputs = tf.unstack(x, axis=2)
        rnn_inputs_new = []
        for rx in rnn_inputs:
            rnn_inputs_new.append(tf.transpose(rx))

        state_placeholder = tf.placeholder(tf.float32, [num_layers, 2, batch_size, state_size])
        l = tf.unstack(state_placeholder, axis=0)
        rnn_tuple_state = tuple(
            [tf.contrib.rnn.LSTMStateTuple(l[idx][0], l[idx][1])
             for idx in range(num_layers)]
        )
    cell = Q_BasicLSTMCell_with_normalize(state_size)
    cell = tf.contrib.rnn.DropoutWrapper(cell, input_keep_prob=0.95, output_keep_prob=0.95)
    cell = tf.contrib.rnn.MultiRNNCell([cell] * num_layers, state_is_tuple=True)

    rnn_outputs, final_state = tf.contrib.rnn.static_rnn(cell, rnn_inputs_new, initial_state=rnn_tuple_state)

    with tf.variable_scope('softmax'):
        W = tf.get_variable('W', [state_size, num_classes])
        b = tf.get_variable('b', [num_classes], initializer=tf.constant_initializer(0.0))

    with tf.name_scope('Activation'):
        logits = [tf.matmul(rnn_output, W) + b for rnn_output in rnn_outputs]
        predictions0 = [tf.nn.softmax(logit) for logit in logits]
        predictions = [tf.cast(tf.argmax(a, 1), tf.int32, name='pred') for a in predictions0]
        pred_for_test = tf.stack(predictions, axis=0, name='pred_for_test')

    with tf.name_scope('train'):
        losses = [tf.nn.sparse_softmax_cross_entropy_with_logits(labels=label, logits=logit) for \
                  logit, label in zip(logits, y_as_list)]
        total_loss = tf.reduce_mean(losses)
        train_step = tf.train.AdagradOptimizer(learning_rate).minimize(total_loss)
        correct_pred = tf.equal(y_as_list, predictions)
        accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

    return dict(x=x, y=y, state_placeholder=state_placeholder, total_loss=total_loss, losses=losses,
                final_state=final_state, train_step=train_step, accuracy=accuracy,
                prediction=predictions, pred_for_test=pred_for_test)


def train_network(data, g, num_steps, num_layers, state_size, batch_size, verbose=True):
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        training_losses = []
        training_accuracies = []
        out_pred = pd.Series()
        training_loss = 0
        training_accuracy = 0
        training_state = np.zeros((num_layers, 2, batch_size, state_size))

        epoch = gen_batchND(data, batch_size, num_steps)

        for step, (X, Y) in enumerate(epoch):
            # print('step=',step)
            feed_dict = {g['x']: X, g['y']: Y, g['state_placeholder']: training_state}
            tr_losses, training_loss_, training_state, TS, accuracy_, pred_ = \
                sess.run(
                    [g['losses'], g['total_loss'], g['final_state'], g['train_step'], g['accuracy'], g['prediction']],
                    feed_dict=feed_dict)
            training_loss += training_loss_
            training_accuracy += accuracy_
            new_items = {(100 * (1 + step) + i): x[0] for i, x in enumerate(pred_)}
            out_pred = out_pred.append(pd.Series(new_items))

            if step > 0:
                if verbose:
                    # print('Accuracy',step,training_accuracy)
                    training_losses.append(training_loss)
                    training_loss = 0
                    training_accuracies.append(training_accuracy)
                    training_accuracy = 0
                    # print(training_state)

        print('yes')
        saver = tf.train.Saver()
        saver.save(sess, meta_graph_path)
        print(sess.run(g['pred_for_test'], feed_dict={g['x']: X, g['state_placeholder']: training_state}))
    return dict(final_state=training_state, out_pred=out_pred)


def cal_pred_ret(x_ret, y_pred, sub):
    x_ret = x_ret.reset_index(drop=True)
    y_pred = y_pred.reset_index(drop=True)
    sub_buy = np.zeros(len(y_pred))
    for i in sub:
        if (y_pred[i] == 1):
            sub_buy[i:(i + 9)] = 1
    x_ret.iloc[y_pred.index[sub_buy == 0]] = 0
    return x_ret


def cal_buy_range(df_y):
    df_y = df_y.reset_index(drop=True)
    buy_range = {}
    key = -1
    for i in range(len(df_y)):
        if (df_y[i] == 1):
            if key == -1:
                key = i
            else:
                next
        else:
            if key == -1:
                next
            else:
                value = i
                buy_range.update({key: value})
                key = -1
    return buy_range


def get_train(df, num_steps):
    df['HIGH'] = df.HIGH / df.CLOSE[0]
    df['LOW'] = df.LOW / df.CLOSE[0]
    df['CLOSE'] = df.CLOSE / df.CLOSE[0]
    df['MA_5'] = df.CLOSE.rolling(5).mean()
    df['STD'] = df.CLOSE.rolling(5).apply(lambda x: np.std(x, ddof=1))
    df['b_pect'] = (df.CLOSE - df.MA_5) / (2 * df.STD)
    df['pch'] = df.CLOSE.pct_change()
    df['pch_5'] = df.pch.rolling(5).sum()
    df['pch_20'] = df.pch.rolling(20).sum()
    df['std_5'] = df.STD / df.MA_5
    df['SWING'] = (df.HIGH - df.LOW) / df.CLOSE  # * (1+df.pch)
    df['ft_5_20'] = df.FREE_TURN.rolling(5).mean() - df.FREE_TURN.rolling(20).mean()
    df['volume_5_20'] = df.VOLUME.rolling(5).mean() - df.VOLUME.rolling(20).mean()
    df['cMA'] = df.CLOSE.rolling(11).mean()  ## 7 for step=6
    df['Y'] = 1
    sub_y = df.columns.get_loc('Y')
    for i in range(100, df.shape[0] - 10):
        if ((df.cMA[i] > df.CLOSE[i]) & (df.cMA[i + 5] > df.cMA[i + 3])):
            df.iloc[i, sub_y] = 1
        elif ((df.cMA[i] < df.CLOSE[i]) & (df.cMA[i + 5] < df.cMA[i + 3])):
            df.iloc[i, sub_y] = 0
        else:
            df.iloc[i, sub_y] = df.iloc[i - 1, sub_y]

    df_train = df[['SWING', 'b_pect', 'pch', 'pch_5', 'pch_20', 'std_5', 'ft_5_20', 'volume_5_20', 'Y']]
    df_train = df_train.loc[4000:(df.shape[0] - num_steps)]
    df_train = df_train.reset_index(drop=True)
    return df_train


num_steps = 10
num_classes = 2
state_size = 8
num_layers = 3
sql_query = "select * from wind_index_daily where wind_code = '000001.SH' and trade_date < '2017-05-23'"
lstm_tuple_path = r"d:/Downloads/lstm_tuple.pickle"
meta_graph_path = r"D:/Downloads/lstm"

engine = get_db_engine()

df = pd.read_sql_query(sql_query, engine)
D = get_train(df, num_steps)
p_num = D.shape[1] - 1

g = build_graph(p_num=p_num, num_steps=num_steps, batch_size=1, num_classes=num_classes,
                state_size=state_size, learning_rate=0.01, num_layers=num_layers)
predicted = train_network(data=D, g=g, num_steps=num_steps, num_layers=num_layers, state_size=state_size, batch_size=1)
lstm_tuple_final = predicted['final_state']
historical_out_sample_pred = predicted['out_pred']

for i in range(1, len(lstm_tuple_final)):
    if i == 1:
        lstm_ndarray = np.append([np.array([lstm_tuple_final[0][0], lstm_tuple_final[0][1]])],
                                 [np.array([lstm_tuple_final[1][0], lstm_tuple_final[1][1]])], axis=0)
    else:
        lstm_ndarray = np.append(lstm_ndarray, [np.array([lstm_tuple_final[i][0], lstm_tuple_final[i][1]])], axis=0)
lstm_ndarray.dump(lstm_tuple_path)
