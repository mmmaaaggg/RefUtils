#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/2/25 14:09
@File    : chinese_char_plot.py
@contact : mmmaaaggg@163.com
@desc    : matlab 显示中文问题
font                                                    解决 plt.plot 中文问他
mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']   解决 DataFrame.plot 中文图例问题，但是图例英文显示会出现问他，因此建议不要使用中文图例
"""
import platform

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.font_manager import FontProperties
from pylab import mpl

# font 解决 plt.plot 中文问他
if platform.system() == 'Windows':
    # 调用系统字体  C:\WINDOWS\Fonts
    font = FontProperties(fname=r"C:\\WINDOWS\\Fonts\\FZSTK.TTF", size=14)
else:
    font = FontProperties(fname='/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf')

# t = np.linspace(0, 10, 1000)
# y = np.sin(t)
# plt.plot(t, y)
# plt.xlabel(u"时间", fontproperties=font)
# plt.ylabel(u"振幅", fontproperties=font)
# plt.title(u"正弦波", fontproperties=font)

data_df = pd.DataFrame({"线段a": [1, 2, 3], '线段b': [3, 2, 1]})

mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']    # 指定默认字体：解决plot不能显示中文问题

data_df.plot(title='中文标题')

plt.title(u"正弦波", fontproperties=font)

plt.show()
