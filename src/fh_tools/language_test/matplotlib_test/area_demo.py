#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 19-5-14 上午10:22
@File    : area_demo.py
@contact : mmmaaaggg@163.com
@desc    : 
"""
import matplotlib.pyplot as plt
import pandas as pd

df = pd.DataFrame({'a': [1, 2, 3], 'b': [2, 3, 4], 'c': [3, 4, 5], 'd': [4, 5, 6]})
fig, axes = plt.subplots(3, 1, figsize=(8, 6))

df.plot(ax=axes[0])
df.plot(stacked=True, ax=axes[1])
df.plot.area(colormap='jet', alpha=0.9, ax=axes[2])
plt.show()

if __name__ == "__main__":
    pass
