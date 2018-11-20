#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/11/16 10:39
@File    : list_pop_remove_test.py
@contact : mmmaaaggg@163.com
@desc    : 
"""

aaa = ['q', 's', 'e']
print(aaa)
aaa.pop(2)
print("aaa.pop(2) ok")
try:
    aaa.pop('q')
except TypeError:
    print("aaa.pop('q') error")

aaa = ['q', 's', 'e']
aaa.remove('q')
print("aaa.remove('q') ok")
try:
    aaa.remove(1)
except ValueError:
    print("aaa.remove(1) error")


