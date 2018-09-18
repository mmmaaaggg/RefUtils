#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/2/25 14:09
@File    : chinese_char_plot.py
@contact : mmmaaaggg@163.com
@desc    : matlab 显示中文问题
"""
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pylab import mpl

# 调用系统字体  C:\WINDOWS\Fonts
font = FontProperties(fname=r"C:\\WINDOWS\\Fonts\\FZSTK.TTF", size=14)

# t = np.linspace(0, 10, 1000)
# y = np.sin(t)
# plt.plot(t, y)
# plt.xlabel(u"时间", fontproperties=font)
# plt.ylabel(u"振幅", fontproperties=font)
# plt.title(u"正弦波", fontproperties=font)

data_df = pd.DataFrame({"线段a": [1,2,3], '线段b': [3,2,1]})
data_df.plot(title='中文标题')
plt.title(u"正弦波", fontproperties=font)
plt.show()
