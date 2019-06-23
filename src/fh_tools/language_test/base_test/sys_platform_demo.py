#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2019/5/10 21:29
@File    : sys_platform_demo.py
@contact : mmmaaaggg@163.com
@desc    : 
"""
import platform

print(platform.system())

if platform.system() == 'Windows':
    print('Windows系统')
elif platform.system() == 'Linux':
    print('Linux系统')
else:
    print('其他')
