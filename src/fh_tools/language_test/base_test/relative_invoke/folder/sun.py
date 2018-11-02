#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/11/1 17:35
@File    : sun.py
@contact : mmmaaaggg@163.com
@desc    : 
"""
import os
import sys

print('sys.path:')
for path in sys.path:
    print(path)

if os.path.abspath(os.curdir) not in sys.path:
    sys.path.append(os.path.abspath(os.curdir))
    print("add to path:\n", os.path.abspath(os.curdir))

from parent import call_parent


def call_sun():
    print('here is sun')
    print('sun call parent')
    call_parent()


if __name__ == "__main__":
    call_sun()
