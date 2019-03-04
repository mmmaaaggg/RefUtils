# -*- coding: utf-8 -*-
"""
Created on 2017/11/6
@author: MG
"""
from collections import Iterable


def yf_test(iter_obj):
    yield from iter_obj


def y_yf_test(something):
    for n in something:
        if isinstance(n, Iterable):
            # print('get:', n, 'Iterable')
            yield from n
        else:
            # print('get:', n)
            yield n


yf_ret = yf_test([1, 2, 3, 4, 5])

print('yield from test')
for n in yf_ret:
    print(n, ', ', end='')

print('')
yf_ret = y_yf_test([[1, 2, 3, 4, 5], 6, 7, [8, 9]])

print('yield and yield from test')
for n in yf_ret:
    print(n, ',', end='')
