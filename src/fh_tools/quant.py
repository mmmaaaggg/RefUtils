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


def target_futrue_pct_range(df: pd.DataFrame, pct_label: str, min_pct: float, max_pct: float, target_label='target'):
    """
    根据时间序列数据 df[pct_label] 计算每一个时点目标标示 -1 0 1
    计算方式：当某一点未来波动首先
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


if __name__ == "__main__":
    import numpy as np

    df = pd.DataFrame({"price": np.sin(np.arange(0, 7, 0.3)) + 5})
    df['pct_change'] = df['price'].pct_change()
    df_target = target_futrue_pct_range(df, 'pct_change', -0.1, 0.1)
    print(df_target)
