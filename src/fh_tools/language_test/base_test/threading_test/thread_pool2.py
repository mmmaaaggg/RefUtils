# -*- coding: utf-8 -*-
"""
Created on 2017/7/19
@author: MG
"""
import threadpool

result_list = []


def hello(m, n, o):
    result = "m = %s, n = %s, o = %s" % (m, n, o)
    result_list.append(result)
    print(result)


if __name__ == '__main__':
    # 方法1
    lst_vars_1 = ['1', '2', '3']
    lst_vars_2 = ['4', '5', '6']
    func_var = [(lst_vars_1, None), (lst_vars_2, None)]
    # 方法2
    dict_vars_1 = {'m': '1', 'n': '2', 'o': '3'}
    dict_vars_2 = {'m': '4', 'n': '5', 'o': '6'}
    func_var = [(None, dict_vars_1), (None, dict_vars_2)]

    pool = threadpool.ThreadPool(2)
    requests = threadpool.makeRequests(hello, func_var)
    [pool.putRequest(req) for req in requests]
    pool.wait()
    print(result_list)
