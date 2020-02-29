#! /usr/bin/env python3
"""
@author  : MG
@Time    : 2020/2/29 上午11:25
@File    : decorate_on_class_init.py
@contact : mmmaaaggg@163.com
@desc    : 在类上加装饰器,修改init方法
"""
import types


def dec_class(cls):
    print(isinstance(cls, type))
    org_init = cls.__init__

    def new_func(self, tail):
        print('***' + ' ' + tail)

    def wrapper_func(self, param):
        org_init(self, param)

        if param == 'fuck':
            self.foo = types.MethodType(new_func, self)

    cls.__init__ = wrapper_func
    return cls


@dec_class
class AClass:

    def __init__(self, param):
        self.param = param

    def foo(self, tail):
        print(self.param + ' ' + tail)


if __name__ == "__main__":
    aaa = AClass('call')
    aaa.foo('me')

    aaa = AClass('fuck')
    aaa.foo('me')
