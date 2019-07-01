#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 19-7-1 下午3:12
@File    : df_rolling_demo.py
@contact : mmmaaaggg@163.com
@desc    : 
"""
import pandas as pd


def demo():
    data_len = 10
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
    r_df = pd.DataFrame([df['a'].rolling(window=5).sum(),
                         df['b'].rolling(window=5, min_periods=3).min(),
                         df['c'].rolling(window=5, center=True).mean(),
                         ], index=['a sum', 'b min', 'c mean']).T
    print("r_df\n", r_df)

    print("df.rolling(window=4).mean()\n", df.rolling(window=4).mean())
    print("df.rolling(window=4, on='a').mean()\n", df.rolling(window=4, on='a').mean())
    print("df.rolling(window=4, on='b').mean()\n", df.rolling(window=4, on='b').mean())

    def func(data):
        print('func invoke:', data)
        return sum(data)

    rolling = df.rolling(window=4)
    rolling.apply(func)
    print('无法进行For循环')
    for x in rolling:
        print('for: ', x)


if __name__ == "__main__":
    demo()
