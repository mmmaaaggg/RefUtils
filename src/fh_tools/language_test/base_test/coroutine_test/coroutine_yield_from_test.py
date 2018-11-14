# -*- coding: utf-8 -*-
"""
Created on 2018/11/12
@author: MG
"""
from src.fh_tools.fh_utils import active_coroutine


def averager():
    # print('active func')
    data_list, data_count = [], 0
    while True:
        print('get data')
        i = yield
        print('get data:', i)
        if i is None:
            break
        data_list.append(i)
        data_count += 1
    ret = sum(data_list) / data_count
    print('return', ret)
    return ret


def cor():
    print('start cor')
    ret = yield from averager()
    print('yield from averager():', ret)
    return ret


@active_coroutine
def cor_activated():
    print('start cor')
    ret = yield from averager()
    print('yield from averager():', ret)
    return ret


def main(auto_active=True):
    data_list = [12, 3, 54, 4]
    print('start main')
    if auto_active:
        func = cor_activated()
    else:
        func = cor()
        print('next(func)')
        next(func)

    try:
        for n in data_list:
            print('func.send(%d)' % n)
            func.send(n)
        print('func.send(None)')
        func.send(None)
    except StopIteration as exp:
        print('average is ', exp.value)


if __name__ == '__main__':
    main()
