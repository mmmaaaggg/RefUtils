#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/11/1 17:43
@File    : main.py
@contact : mmmaaaggg@163.com
@desc    : 
"""

import os
import sys

print('here is main')
print('sys.path:')
for path in sys.path:
    print(path)

# if os.path.abspath(os.curdir) in sys.path:
#     sys.path.append(os.path.abspath(os.curdir))
#     print("add to path:\n", os.path.abspath(os.curdir))


from folder.sun import call_sun
call_sun()
