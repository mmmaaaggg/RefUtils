#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 19-4-15 上午9:02
@File    : check_before_run.py
@contact : mmmaaaggg@163.com
@desc    : 
"""


def check_func():
    print('check before call')
    return True


def check_before_run(func):

    def func_warpper(f):

        def call_func(*args, **kwargs):
            is_ok = func()
            if is_ok:
                print('checked')
                return f(*args, **kwargs)
            else:
                print('check failed')
                raise ImportError('check failed')

        return call_func

    return func_warpper


@check_before_run(check_func)
def AMethod(name):
    print('run AMethod', name)


if __name__ == "__main__":
    print('call AMethod')
    AMethod('abc')
