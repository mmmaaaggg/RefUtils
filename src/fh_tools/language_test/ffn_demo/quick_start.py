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

data = ffn.get('agg,hyg,spy,eem,efa', start='2010-01-01', end='2014-01-01')
print(data.head())

