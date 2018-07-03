#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/2/27 17:22
@File    : ggplot_test.py
@contact : mmmaaaggg@163.com
@desc    : 
"""

from ggplot import *
diamonds.head()

p = ggplot(aes(x='date', y='beef'), data=meat)
p + geom_point()
p + geom_point() + geom_line()
p + geom_point() + geom_line() + stat_smooth(color='blue')

