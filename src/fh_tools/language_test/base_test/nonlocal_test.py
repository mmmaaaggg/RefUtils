# -*- coding: utf-8 -*-
"""
Created on 2017/9/30
@author: MG
全局作用域（global）：在整个程序运行环境中都可见
@description: nonlocal global 两个关键字
nonlocal，指定上一级变量，如果没有就继续往上直到找到为止
global, 函数中有global关键字，变量本质上就是全局变量，可读取可赋值
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
