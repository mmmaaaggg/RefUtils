#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2019/3/14 15:35
@File    : quant.py
@contact : mmmaaaggg@163.com
@desc    : 量化分析相关工具
"""
import pandas as pd
import numpy as np


def add_target_future_pct_range(df: pd.DataFrame, pct_label: str, min_pct: float, max_pct: float, target_label='target'):
    """
    根据时间序列数据 df[pct_label] 计算每一个时点目标标示 -1 0 1
    计算方式：当某一点未来波动首先 >（ 或 <） 上届 min_pct（或下届 max_pct），则标记为 1 （或 -1）
    :param df:
    :param pct_label:
    :param min_pct:
    :param max_pct:
    :param target_label:
    :return:
    """
    pct_s = df[pct_label]
    cum_rr = (pct_s + 1).cumprod().fillna(1)
    target_s = np.zeros(cum_rr.shape)
    for i in range(cum_rr.shape[0]):
        base = cum_rr[i]
        for j in range(i + 1, cum_rr.shape[0]):
            result = cum_rr.iloc[j] / base - 1
            if result < min_pct:
                target_s[i] = -1
                break
            elif result > max_pct:
                target_s[i] = 1
                break

    df[target_label] = target_s
    return df


def get_target_by_future_pct_range(pct_arr: np.ndarray, min_pct: float, max_pct: float):
    """
    根据时间序列数据 pct_arr 计算每一个时点目标标示 -1 0 1
    计算方式：当某一点未来波动首先 >（ 或 <） 上届 min_pct（或下届 max_pct），则标记为 1 （或 -1）
    :param pct_arr:
    :param min_pct:
    :param max_pct:
    :return:
    """
    pct_arr[np.isnan(pct_arr)] = 0
    cum_rr = (pct_arr + 1).cumprod()
    arr_len = cum_rr.shape[0]
    target_arr = np.zeros(cum_rr.shape)
    for i in range(arr_len):
        base = cum_rr[i]
        for j in range(i + 1, arr_len):
            result = cum_rr[j] / base - 1
            if result < min_pct:
                target_arr[i] = -1
                break
            elif result > max_pct:
                target_arr[i] = 1
                break

    return target_arr


if __name__ == "__main__":

    df = pd.DataFrame({"price": np.sin(np.arange(0, 7, 0.3)) + 5})
    df['pct_change'] = df['price'].pct_change()
    df_target = add_target_future_pct_range(df, 'pct_change', -0.1, 0.1)
    print("df_target:\n", df_target)

    pct_arr = df['pct_change'].to_numpy()
    target_arr = get_target_by_future_pct_range(pct_arr, -0.1, 0.1)
    print("target_arr:\n", target_arr)

