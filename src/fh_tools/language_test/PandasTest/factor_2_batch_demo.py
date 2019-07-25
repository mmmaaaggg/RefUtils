#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 19-7-1 下午4:21
@File    : factor_2_batch_demo.py
@contact : mmmaaaggg@163.com
@desc    : 演示如何将一个 DataFrame (8, 3) 循环叠加转换成 (4, 5, 3)
"""
import pandas as pd
import numpy as np


def demo():
    data_len = 8
    date_arr = pd.date_range(pd.to_datetime('2018-01-01'),
                             pd.to_datetime('2018-01-01') + pd.Timedelta(days=data_len * 2 - 1),
                             freq=pd.Timedelta(days=2))
    date_index = pd.DatetimeIndex(date_arr)
    df = pd.DataFrame(
        {'a': list(range(data_len)),
         'b': list(range(data_len*2, data_len * 3)),
         'c': list(range(data_len * 10, data_len * 11))},
        index=date_index,
    )
    print("df\n", df)
    n_step = 5
    factor_index, factor_columns = df.index[(n_step - 1):], df.columns
    new_shape = [df.shape[0] - n_step + 1, n_step]
    new_shape.extend(df.shape[1:])
    new_shape = tuple(new_shape)
    print("df.shape:", df.shape)
    print("new_shape:", new_shape)
    factor_arr_batch, factor_arr = np.zeros(new_shape), df.to_numpy()
    for idx_from, idx_to in enumerate(range(n_step, factor_arr.shape[0] + 1)):
        factor_arr_batch[idx_from] = factor_arr[idx_from: idx_to]
    print('new reshaped factor_arr_batch')
    print(factor_arr_batch)
    print("factor_index", factor_index)


if __name__ == "__main__":
    demo()
