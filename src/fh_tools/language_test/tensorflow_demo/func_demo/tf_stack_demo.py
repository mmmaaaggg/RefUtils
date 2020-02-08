#! /usr/bin/env python3
"""
@author  : MG
@Time    : 2020/2/8 下午4:43
@File    : tf_stack_demo.py
@contact : mmmaaaggg@163.com
@desc    :
版权声明：本文为CSDN博主「feifeiyechuan」的原创文章，遵循
CC 4.0 BY - SA
版权协议，转载请附上原文出处链接及本声明。
原文链接：https: // blog.csdn.net / feifeiyechuan / article / details / 89388103

"""
import tensorflow as tf
import numpy as np

with tf.compat.v1.Session() as sess:
    # sess.run(tf.compat.v1.global_variables_initializer())

    # stack and unstack
    stack_data1, stack_data2 = np.arange(1, 31).reshape([2, 3, 5])
    print('stack_data1: \n', stack_data1)
    print('stack_data1.shape: \n', stack_data1.shape)
    print('stack_data2: \n', stack_data2)
    print('stack_data2.shape: \n', stack_data2.shape)
    # stack_data1:
    #  [[ 1  2  3  4  5]
    #  [ 6  7  8  9 10]
    #  [11 12 13 14 15]]
    # stack_data1.shape:
    #  (3, 5)
    # stack_data2:
    #  [[16 17 18 19 20]
    #  [21 22 23 24 25]
    #  [26 27 28 29 30]]
    # stack_data2.shape:
    #  (3, 5)

    # 理解：
    #     举例：当前两个个张量的维度均为：（维1，维2， 维3， 维4）， 此时axis的取值范围为：[-5, 5)
    #     所以输入 stacks = [stack_data1, stack_data2], st = tf.stack(stacks, axis=?)
    #     此时：
    #           stacks的维度为：（2，维1，维2， 维3， 维4 ）   维度为5，所以输出维度也为5， axis取值就在[-5, 5)
    #           当axis=0时， st维度为：（2, 维1， 维2， 维3， 维4）
    #           当axis=1时， st维度为：（维1， 2，维2， 维3， 维4）
    #           当axis=2时， st维度为：（维1， 维2， 2，维3， 维4）
    #           当axis=3时， st维度为：（维1， 维2， 维3，2，维4）
    #           当axis=4时， st维度为：（维1， 维2， 维3，维4，2）

    #           当axis=-5时， st维度为：（2, 维1， 维2， 维3， 维4）
    #           当axis=-4时， st维度为：（维1， 2，维2， 维3， 维4）
    #           当axis=-3时， st维度为：（维1， 维2， 2，维3， 维4）
    #           当axis=-2时， st维度为：（维1， 维2， 维3，2，维4）
    #           当axis=-1时， st维度为：（维1， 维2， 维3，维4，2）

    print('======================================')
    st_0 = tf.stack([stack_data1, stack_data2], axis=0)  # 2 * (3, 5) ==> (2, 3, 5)
    st_0 = sess.run(st_0)
    print('st_0: \n', st_0)
    print('st_0.shape: \n', st_0.shape)
    # st_0:
    #  [[[ 1  2  3  4  5]
    #   [ 6  7  8  9 10]
    #   [11 12 13 14 15]]
    #
    #  [[16 17 18 19 20]
    #   [21 22 23 24 25]
    #   [26 27 28 29 30]]]
    # st_0.shape:
    #  (2, 3, 5)

    print('======================================')
    st_1 = tf.stack([stack_data1, stack_data2], axis=1)  # 2 * (3, 5) ==> (3, 2, 5)
    st_1 = sess.run(st_1)
    print('st_1: \n', st_1)
    print('st_1.shape: \n', st_1.shape)
    # st_1:
    #  [[[ 1  2  3  4  5]
    #   [16 17 18 19 20]]
    #
    #  [[ 6  7  8  9 10]
    #   [21 22 23 24 25]]
    #
    #  [[11 12 13 14 15]
    #   [26 27 28 29 30]]]
    # st_1.shape:
    #  (3, 2, 5)

    print('======================================')
    st_2 = tf.stack([stack_data1, stack_data2], axis=2)  # 2 * (3, 5) ==> (3, 5, 2)
    st_2 = sess.run(st_2)
    print('st_2: \n', st_2)
    print('st_2.shape: \n', st_2.shape)
    # st_2:
    #  [[[ 1 16]
    #   [ 2 17]
    #   [ 3 18]
    #   [ 4 19]
    #   [ 5 20]]
    #
    #  [[ 6 21]
    #   [ 7 22]
    #   [ 8 23]
    #   [ 9 24]
    #   [10 25]]
    #
    #  [[11 26]
    #   [12 27]
    #   [13 28]
    #   [14 29]
    #   [15 30]]]
    # st_2.shape:
    #  (3, 5, 2)

    print('======================================')
    st_1_ = tf.stack([stack_data1, stack_data2], axis=-1)  # 2 * (3, 5) ==>  (3, 5, 2)   等同于st_2
    st_1_ = sess.run(st_1_)
    print('st_1_: \n', st_1_)
    print('st_1_.shape: \n', st_1_.shape)
    # st_1:
    #  [[[ 1 16]
    #   [ 2 17]
    #   [ 3 18]
    #   [ 4 19]
    #   [ 5 20]]
    #
    #  [[ 6 21]
    #   [ 7 22]
    #   [ 8 23]
    #   [ 9 24]
    #   [10 25]]
    #
    #  [[11 26]
    #   [12 27]
    #   [13 28]
    #   [14 29]
    #   [15 30]]]
    # st_1.shape:
    #  (3, 5, 2)

    print('=================比较st_1, 和 transpose=====================')
    print('st_1: \n', st_1)
    transpose_test = sess.run(tf.transpose(st_0, [1, 0, 2]))
    print('transpose_test: \n', transpose_test)
    print('transpose_test == st_1: \n', transpose_test == st_1)

    print('=================比较st_2, 和 transpose=====================')
    print('st_2: \n', st_2)
    transpose_test = sess.run(tf.transpose(st_0, [1, 2, 0]))
    print('transpose_test: \n', transpose_test)
    print('transpose_test == st_2: \n', transpose_test == st_2)
    # 总结：
    #     tf.stack() 中 stacks = (2，维1，维2， 维3， 维4 ）
    #     当axis=0时， 就相当于tf.transpose(stacks, [0, 1, 2, 3, 4])
    #     当axis=1时， 就相当于tf.transpose(stacks, [1, 0, 2, 3, 4])
    #     当axis=2时， 就相当于tf.transpose(stacks, [1, 2, 0, 3, 4])
    #     当axis=3时， 就相当于tf.transpose(stacks, [1, 2, 3, 0, 4])
    #     当axis=0时， 就相当于tf.transpose(stacks, [1, 2, 3, 4, 0])


    # 4 维测试：
    stack_data1, stack_data2 = np.arange(1, 121).reshape([2, 3, 4, 5])  # (2, 3, 4, 5)
    st_ = tf.stack([stack_data1, stack_data2], axis=3)
    st_0 = tf.stack([stack_data1, stack_data2], axis=0)
    st_ = sess.run(st_)
    st_0 = sess.run(st_0)

    tr_ = tf.transpose(st_0, [1, 2, 3, 0])
    tr_ = sess.run(tr_)

    print('st_.shape: ', st_.shape)
    print('st_: ', st_)

    print('tr_.shape: ', tr_.shape)
    print('tr_: ', tr_)

    print(st_ == tr_)

if __name__ == "__main__":
    pass
