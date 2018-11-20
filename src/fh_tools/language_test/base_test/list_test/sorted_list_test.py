#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/11/15 19:35
@File    : sorted_list_test.py
@contact : mmmaaaggg@163.com
@desc    : 对列表元素进行排序
"""
from src.fh_tools.fh_utils import str_2_datetime

aaa = [
    (str_2_datetime('2018-5-6 12:32:34'), 'd'),
    (str_2_datetime('2018-7-6 12:32:34'), 'e'),
    (str_2_datetime('2018-5-6 1:52:34'), 'c'),
    (str_2_datetime('2018-1-6 12:32:34'), 'a'),
    (str_2_datetime('2018-5-6 1:32:34'), 'b'),
]

aaa.sort(key=lambda x: x[0])
for a in aaa:
    print(a)
