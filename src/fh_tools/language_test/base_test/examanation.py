#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 19-9-18 上午11:54
@File    : examanation.py
@contact : mmmaaaggg@163.com
@desc    : 
"""


def iterator(x):
    print(f'iter {x:03d} start')
    rets = []
    for _ in range(0, x, 2):
        rets.append((_ ** 2) // 3)
        yield rets
    print(f'iter {x:03d} finish')


def main():
    print('start')
    _iter = iterator(6)
    for _ in _iter:
        print(_)
    print('end')


# def main():
#     for _, x in enumerate('Hello World'):
#         if _ % 3 == 0:
#             print('%02d -> %s' % (_, x))


if __name__ == "__main__":
    main()
