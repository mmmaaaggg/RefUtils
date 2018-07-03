# -*- coding: utf-8 -*-
"""
Created on 2017/9/30
@author: MG
"""

def make_averager():
    count = 0
    total = 0

    def averager(new_value):
        nonlocal count, total
        count += 1
        total += new_value
        return total / count

    return averager

if __name__ == "__main__":
    avg = make_averager()
    print("avg(10)", avg(10))
    print("avg(12)", avg(12))
