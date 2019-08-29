#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 19-8-9 上午10:33
@File    : grades_demo.py
@contact : mmmaaaggg@163.com
@desc    : 通过二分发计算分数等级
"""
import bisect


def grade(score, breakpoints=[60, 70, 80, 90], grades='FDCBA'):
    i = bisect.bisect(breakpoints, score)
    return grades[i]


print([grade(score) for score in [33, 99, 77, 70, 89, 90, 100]])

if __name__ == "__main__":
    pass
