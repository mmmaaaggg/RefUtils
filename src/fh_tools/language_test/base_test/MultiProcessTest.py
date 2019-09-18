#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/6/23 11:19
@File    : MultiProcessTest.py
@contact : mmmaaaggg@163.com
@desc    : https://www.jianshu.com/p/ef8c0a4e2049
"""

import time
from datetime import datetime
from multiprocessing import Pool, context


def f(x):
    print('x is %d, %s' % (x, datetime.now()))
    time.sleep(1)
    return x * x


if __name__ == '__main__':
    pool = Pool(processes=4)  # start 4 worker processes

    result0 = pool.apply_async(f, (10,))  # evaluate "f(10)" asynchronously in a single process
    result = pool.apply_async(f, (11,))  # evaluate "f(10)" asynchronously in a single process
    result = pool.apply_async(f, (12,))  # evaluate "f(10)" asynchronously in a single process
    result = pool.apply_async(f, (13,))  # evaluate "f(10)" asynchronously in a single process
    result = pool.apply_async(f, (14,))  # evaluate "f(10)" asynchronously in a single process
    result = pool.apply_async(f, (15,))  # evaluate "f(10)" asynchronously in a single process
    print('result.get(timeout=3)', result0.get(timeout=3))  # prints "100" unless your computer is *very* slow


    print('pool.map(f, list(range(10)))', pool.map(f, list(range(10))))  # prints "[0, 1, 4,..., 81]"

    it = pool.imap(f, list(range(10)))
    print('next(it)', next(it))  # prints "0"
    print('next(it)', next(it))  # prints "1"
    print('it.next(timeout=1)', it.next(timeout=1))  # prints "4" unless your computer is *very* slow


    try:
        result = pool.apply_async(time.sleep, (10,))
        print(result.get(timeout=1))  # raises multiprocessing.TimeoutError
    except context.TimeoutError:
        print('result.get()', result.get())
