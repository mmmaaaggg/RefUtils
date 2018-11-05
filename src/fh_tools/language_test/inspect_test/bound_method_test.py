#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/11/5 9:32
@File    : bound_method_test.py
@contact : mmmaaaggg@163.com
@desc    : 
"""
import inspect


class AClass:

    def func(self):
        print('bound method')


def test():
    print("AClass.func is method:", inspect.ismethod(AClass.func))
    instance = AClass()
    print("AClass.func is method:", inspect.ismethod(instance.func))
    print("getattr(AClass, 'func') is method:", inspect.ismethod(getattr(AClass, 'func')))
    print("getattr(instance, 'func') is method:", inspect.ismethod(getattr(instance, 'func')))


if __name__ == "__main__":
    test()
