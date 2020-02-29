#! /usr/bin/env python3
"""
@author  : MG
@Time    : 2020/2/29 上午11:55
@File    : check_class_type.py
@contact : mmmaaaggg@163.com
@desc    : 判断传入的对象是 类或方法
"""
import types


class AClass:
    pass


def func():
    pass


print(isinstance(AClass, type))

print(isinstance(func, types.FunctionType))

if __name__ == "__main__":
    pass
