# -*- coding:utf-8 -*-

import pandas as pd
import numpy as np

# s1 = pd.Series(list(range(4)), index=['b', 'd', 'c', 'a'])
s1 = pd.Series({'a': 0, 'b': 1, 'c': 2, 'd': 3}, name='s1')
print("s1 = pd.Series({'a': 0, 'b': 1, 'c': 2, 'd': 3}, name='s1') is")
print(s1)
print("s1['a']:", s1['a'])
print("s1.iloc[1]:", s1.iloc[1])
s1.to_csv('s1.csv')
s1.to_csv('s1_noindex.csv', index=False, header=True)

s2 = pd.Series([3, 4, np.inf, np.nan], index=['c', 'd', 'e', 'f'])
print('s2\n', s2)
print('s2 has nan count', sum(np.isnan(s2)))
print('s2.fillna(0)', s2.fillna(0))
s2[np.isinf(s2)] = 0
print('s2[np.isinf(s2)]=0', s2)
s1.rename('as2df')

df = pd.DataFrame(s1, columns=['Col1'])
df['Col2'] = s2
print('e 行数据丢失', df)
print("df['Col2'].mean() =", df['Col2'].mean())
print("df['Col2'].fillna(0) =", df['Col2'].fillna(0))
df = pd.DataFrame([s1, s2], index=['C1', 'C2']).T
print("pd.DataFrame([s1, s2], index=['C1', 'C2']).T\n", df)

df = pd.DataFrame({'C1': s1, 'C2': s2})
print(df)
