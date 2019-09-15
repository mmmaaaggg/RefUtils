#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 19-8-9 上午10:24
@File    : bisect_find.py
@contact : mmmaaaggg@163.com
@desc    : 插入排序及二分法查找
"""
import bisect
import random

random.seed(1)

print('New Pos Contents')

print('--- --- --------')

l = []
for i in range(1, 15):
    r = random.randint(1, 100)
    position = bisect.bisect(l, r)
    bisect.insort(l, r)
    print('%3d %3d' % (r, position), l)


def binary_search_bisect(lst, x):
    from bisect import bisect_left
    i = bisect_left(lst, x)
    if i != len(lst) and lst[i] == x:
        return i
    return None


if __name__ == "__main__":
    assert binary_search_bisect(l, 18) == 3
    assert binary_search_bisect(l, 9) == 0
    assert binary_search_bisect(l, 98) == 12
    assert binary_search_bisect(l, 99) is None
    assert binary_search_bisect(l, 97) is None
    assert binary_search_bisect(l, 1) is None
