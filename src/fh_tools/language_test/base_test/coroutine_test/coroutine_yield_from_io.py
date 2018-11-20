#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/11/15 15:25
@File    : coroutine_yield_from_io.py
@contact : mmmaaaggg@163.com
@desc    : 
"""
from src.fh_tools.fh_utils import active_coroutine


def calc_func(do=True):
    data_list = []
    result = 0
    while do:
        x = yield result
        if x is None:
            break
        result = x * 2
        data_list.append(result)

    return sum(data_list)


@active_coroutine
def cor_activated(do=True):
    print('start cor')
    ret = yield from calc_func(do)
    print('yield from calc_func():', ret)
    return ret


def main():

    try:
        cor = cor_activated(True)
        for n in range(5):
            ret = cor.send(n)
            print("cor.send(%d) return:" % n, ret)
        cor.send(None)
    except StopIteration as exp:
        print("exp.value:", exp.value)


if __name__ == "__main__":
    main()
