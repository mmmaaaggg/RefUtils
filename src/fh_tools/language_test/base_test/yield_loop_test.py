#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/11/15 19:53
@File    : yield_loop_test.py
@contact : mmmaaaggg@163.com
@desc    : 
"""


def yield_loop(n):
    for x in range(n):
        yield x * 2
    print('loop finished')
    return n


def main():
    looper = yield_loop(5)

    for num, x in enumerate(looper, start=1):
        print('%d) %d' % (num, x))

    try:
        looper.__next__()
    except StopIteration as exp:
        print('return value', exp.value)  # None 没有返回结果


if __name__ == "__main__":
    main()
