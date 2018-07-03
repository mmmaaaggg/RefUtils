# -*- coding:utf-8 -*-
'''
Created on 2016年12月28日

@author: Family
'''
from datetime import date, datetime, timedelta
import pandas as pd
import numpy as np
from math import isnan

weight = {
    's1': np.random.random(6),
    's2': np.random.random(6),
    's3': np.random.random(6),
    's4': np.random.random(6),
}
date_base = datetime.strptime('2016-1-1', '%Y-%m-%d').date()
day_1 = timedelta(days=1)
date_index = [date_base,
              date_base + day_1,
              date_base + day_1 * 2,
              date_base + day_1 * 3,
              date_base + day_1 * 4,
              date_base + day_1 * 5]
df1 = pd.DataFrame(weight, index=['a', 'b', 'c', 'd', 'e', 'f'])
print('df1\n', df1)

# aaa = [[df1.ix[row_num, 0], df1.ix[row_num, 1]] for row_num in range(df1.shape[0])]
# print(aaa)
# df1.ix[:, [0, 1]].to_dict('splite')
# bbb = [[df1.ix[row_num, 2], df1.ix[row_num, 3]] for row_num in range(df1.shape[0])]
# print(bbb)



print('df1.iloc[[1, 2], :]\n', df1.iloc[[1, 2], :])
print('df1.iloc[:,[1, 2]]\n', df1.iloc[:, [1, 2]])
print("df1[['s1','s2']]\n", df1[['s1', 's2']])
try:
    df1[['s1', 'x2', 'x3']]
except KeyError as exp:
    print("DataFrame:df1[['s1','x2','x3']] cause Key Error【%s】" % exp)
print("df1.ix[['a', 'b']]\n", df1.ix[['a', 'b']])
print("df1.ix[-4].sort_values(ascending=False)\n", df1.ix[-4].sort_values(ascending=False))
print("df1.sort_values('s2')\n", df1.sort_values('s2')[:2].index)
df1['Y_bin'] = -1
df1['Y_bin'][df1.sort_values('s2')[:2].index] = 1
print("df1['Y_bin'][df1.sort_values('s2')[:2].index] = 1 will cause warning")
df1.loc[df1.sort_values('s2').index[2:], 'Y_bin'] = -1
df1.loc[df1.sort_values('s2').index[:2], 'Y_bin'] = 1
print("df1.loc[df1.sort_values('s2')[:2].index, 'Y_bin'] = 1 do the same work and work fine")
print('df1 added Y_bin sort by s2\n', df1)
df2 = df1[df1 > 0.5]
print('df2 = df1[df1>0.5]\n', df2)

print('df2.fillna(0)\n', df2.fillna(0))

print('df1[df1.columns[(df1>0.95).any()]]\n', df1[df1.columns[(df1 > 0.95).any()]])


def checklastbool(x, boolvalue):
    ret = x.dropna() == boolvalue
    return False if len(ret) == 0 else ret.iloc[-1]


# print('df1[df1.columns[df1.iloc[-1]>0.5]]', df1[df1.columns[(df1>0.5).apply(lambda x:checkbool(x, False))]])
print('(df1>0.5).apply(lambda x:checklastbool(x, True))', (df1 > 0.5).apply(lambda x: checklastbool(x, True)))
print('df1[df1.columns[(df1>0.5).apply(lambda x:checkbool(x, True))]]\n',
      df1[df1.columns[(df1 > 0.5).apply(lambda x: checklastbool(x, True))]])
# print('df2.mean(axis=1)', df2.mean(axis=1))

# print('df2.max(axis=1)', df2.max(axis=1))
df1['i1'] = list(range(6))
df1['i2'] = list(range(6, 12))
df1['index'] = df1.index
df2 = df1.set_index(['index', 'i2'])
idxset = set(df2.index.get_level_values('index'))


def calc_quantile(x, qvalue):
    ret = x.dropna().quantile(qvalue)
    return 0 if isnan(ret) else ret


# print('calc_quantile(df2.iloc[0])', calc_quantile(df2.iloc[0]))

# df1.apply(calc_quantile, axis=1)
print('df1.quantile(0.5)\n', df2.apply(lambda x: calc_quantile(x, 0.9), axis=1))

print('df1.iloc[-1]\n', df1.iloc[-1])

df1 = pd.DataFrame(weight, index=date_index)
print(df1.iloc[((date_base + day_1) <= df1.index) & (df1.index <= (date_base + day_1 * 3))])
# print(df1.iloc['2016-01-01' <= df1.index <= '2016-01-04'])

df1 = pd.DataFrame(weight)
df1.index.rename('idx', inplace=True)
print(df1)