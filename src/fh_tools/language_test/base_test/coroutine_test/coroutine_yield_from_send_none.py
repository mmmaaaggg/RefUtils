# -*- coding: utf-8 -*-
"""
Created on 2018/11/12
@author: MG
"""
from src.fh_tools.fh_utils import active_coroutine

data_list = [1, 2, 3, 4, 5]

def averager():
    # print('active func')
    for i, x in enumerate(data_list):
        print(i, ')yield x', x)
        yield x
        print(i, ') yield finished')
    ret = sum(data_list) / len(data_list)
    print('return', ret)
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
    func = cor_activated()

    try:
        for n in data_list:
            print('func.send(%d)' % n)
            func.send(None)  # 不发送数据会出错 TypeError: send() takes exactly one argument (0 given)
        print('func.send(None)')
        func.send(None)
    except StopIteration as exp:
        print('average is ', exp.value)


if __name__ == '__main__':
    main()
