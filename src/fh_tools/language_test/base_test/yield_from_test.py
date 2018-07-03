# -*- coding: utf-8 -*-
"""
Created on 2017/11/6
@author: MG
"""


def yf_test(iter_obj):
    yield from iter_obj


yf_ret = yf_test([1, 2, 3, 4, 5])

for n in yf_ret:
    print(n)
