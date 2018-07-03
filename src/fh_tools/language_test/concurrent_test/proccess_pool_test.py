# -*- coding: utf-8 -*-
"""
Created on 2017/12/12
@author: MG
"""

import time
from concurrent.futures import ProcessPoolExecutor, as_completed
import random


def fib(n, test_arg):
    if n > 30:
        raise Exception('can not > 30, now %s' % n)
    if n <= 2:
        return 1
    return fib(n-1, test_arg) + fib(n-2, test_arg)


def use_submit():
    nums = [random.randint(0, 33) for _ in range(0, 10)]
    with ProcessPoolExecutor() as executor:
        futures = {executor.submit(fib, n, n): n for n in nums}
        for f in as_completed(futures):
            try:
                print('fib(%s) result is %s.' % (futures[f], f.result()))
            except Exception as e:
                print(e)

if __name__ == "__main__":
    use_submit()
