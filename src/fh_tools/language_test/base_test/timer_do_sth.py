#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/8/27 10:21
@File    : timer_do_sth.py
@contact : mmmaaaggg@163.com
@desc    : 定时做一些事情
"""
from datetime import datetime
import time

n = 0
def func():
    global n
    if n < 3:
        n += 1
        raise ValueError('x')
    else:
        n += 1
        print('do sth')


while True:
    dt_now = datetime.now()
    try:
        if dt_now.hour == 10 and dt_now.minute == 39:
            func()
            break
    except Exception as exp:
        print(exp)
    finally:
        time.sleep(1)
