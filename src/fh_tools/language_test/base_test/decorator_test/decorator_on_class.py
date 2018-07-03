#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/6/14 14:18
@File    : decorator_on_class.py
@contact : mmmaaaggg@163.com
@desc    : 
"""


class Foo(object):
    def __init__(self):
        pass

    def __call__(self, func):
        def _call(*args, **kw):
            print('class decorator runing', args, kw)
            return func(*args, **kw)

        return _call


class Bar(object):
    @Foo()
    def bar(self, test, ids):
        print('bar', test, ids)



Bar().bar('aa', 'ids')