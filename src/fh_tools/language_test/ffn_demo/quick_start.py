#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2019/5/9 7:22
@File    : quick_start.py
@contact : mmmaaaggg@163.com
@desc    : http://pmorissette.github.io/ffn/quick.html
"""
import ffn
import matplotlib.pyplot as plt

df = ffn.get('agg,hyg,spy,eem,efa', start='2010-01-01', end='2014-01-01')
print(df.head())

# 归一化走势图
ax = df.rebase().plot()
plt.show()

# 收益率分布图
returns = df.to_returns().dropna()
ax = returns.hist()
plt.show()

stats = df.calc_stats()
print("data.calc_stats().display()\n")
stats.display()

# 回撤图
ax = stats.prices.to_drawdown_series().plot()
plt.show()

stats = df['hyg'].calc_perf_stats()
print("data['hyg'].calc_perf_stats().display()")
stats.display()
