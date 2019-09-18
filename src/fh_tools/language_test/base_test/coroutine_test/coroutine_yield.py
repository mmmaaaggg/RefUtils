#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/11/12 9:21
@File    : coroutine_yield.py
@contact : mmmaaaggg@163.com
@desc    : 
"""


def cor():
    data_list = []
    while True:
        print('go', end='')
        x = yield
        print(x)
        if x is None:
            break
        data_list.append(x)
    ret = sum(data_list) / len(data_list)
    print('average', ret)
    return ret


def main():
    print('call cor()')
    func = cor()
    print('next(func)')
    next(func)
    try:
        for x in range(3):
            print('->', x)
            func.send(x)

        func.send(None)
    except StopIteration as exp:
        print('func return', exp.value)


if __name__ == "__main__":
    main()
