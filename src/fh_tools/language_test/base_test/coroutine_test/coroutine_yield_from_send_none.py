# -*- coding: utf-8 -*-
"""
Created on 2018/11/12
@author: MG
"""
from src.fh_tools.fh_utils import active_coroutine

data_list = [1, 2, 3, 4, 5]


def averager():
    print('active func')
    for i, x in enumerate(data_list):
        print(i, ') yield x ( %d )' % x)
        yield x
        print(i, ') yield x ( %d ) finished' % x)
    ret = sum(data_list) / len(data_list)
    print('return', ret)
    return ret


# @active_coroutine
def cor_activated():
    print('start cor')
    ret = yield from averager()
    print('yield from averager():', ret)
    return ret


def main():
    print('start main')
    func = cor_activated()

    try:
        loop_count = 0
        while True:
            print('%d ) -> func.send(None)' % loop_count)
            ret = func.send(None)  # 不发送数据会出错 TypeError: send() takes exactly one argument (0 given)
            print('%d ) -> return %d' % (loop_count, ret))
            loop_count += 1

    except StopIteration as exp:
        print('loop finished. average is ', exp.value)


def main2():
    print('start main')
    func = cor_activated()

    try:
        loop_count = 0
        for ret in func:
            # print('%d ) -> func.send(None)' % loop_count)
            # ret = func.send(None)  # 不发送数据会出错 TypeError: send() takes exactly one argument (0 given)
            print('%d ) -> return %d' % (loop_count, ret))
            loop_count += 1

    except StopIteration as exp:
        print('loop finished. average is ', exp.value)


if __name__ == '__main__':
    # main()   main2() 两个函数作用相同
    # main()
    main2()

