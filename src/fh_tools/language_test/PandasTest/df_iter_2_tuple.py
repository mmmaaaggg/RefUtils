#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/3/30 10:07
@File    : df_iter_2_tuple.py
@contact : mmmaaaggg@163.com
@desc    : 將 DataFrame 里面的数据转换为 元祖集，便于进行数据比较
"""
import pandas as pd

date_index = {
    'wind_code': ['w' + str(i) for i in range(1, 7)],
    'weight': [i for i in range(1, 7)],
}
df1 = pd.DataFrame(date_index, index=['a', 'b', 'c', 'd', 'e', 'f'])
print(df1)

# for key, val in df1.T.items():
#     print(val)

tuple_set = {tuple(val) for key, val in df1[['wind_code', 'weight']].T.items()}
print(tuple_set)
