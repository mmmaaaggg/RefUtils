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
    print('call check_func')
    return True


def check_before_run(func):
    print('call decorator')

    def func_wrapper(f):

        def call_func(*args, **kwargs):
            is_ok = func()
            if is_ok:
                print('checked')
                return f(*args, **kwargs)
            else:
                print('check failed')
                raise ImportError('check failed')

        return call_func

    return func_wrapper


@check_before_run(check_func)
def a_foo(name):
    print('call a_foo ->', name)


if __name__ == "__main__":
    print('call a_foo start')
    a_foo('abc')
    print('call a_foo end')
