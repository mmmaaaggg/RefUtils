#! /usr/bin/env python3
"""
@author  : MG
@Time    : 2021/3/2 下午10:08
@File    : test_1.py
@contact : mmmaaaggg@163.com
@desc    : 
"""


def solution(A: list):
    counters = [0, 0]
    for n, val in enumerate(A):
        counters[0] += n % 2 == val
        counters[1] += n % 2 != val

    return min(counters)


if __name__ == "__main__":
    solution([1,1,1, 0])
