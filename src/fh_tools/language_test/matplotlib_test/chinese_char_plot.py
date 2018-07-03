#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/2/25 14:09
@File    : chinese_char_plot.py
@contact : mmmaaaggg@163.com
@desc    : matlab 显示中文问题
"""
import matplotlib.pyplot as plt
import pandas as pd
from pylab import mpl


mpl.rcParams['font.sans-serif'] = ['SimHei']  # 字体可以根据需要改动
mpl.rcParams['axes.unicode_minus'] = False  # 解决中文减号不显示的问题
data_df = pd.DataFrame({"线段a": [1,2,3], '线段b': [3,2,1]})
data_df.plot(title='中文标题')
plt.show()
