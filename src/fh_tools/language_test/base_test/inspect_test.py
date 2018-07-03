# -*- coding: utf-8 -*-
"""
Created on 2017/6/13
@author: MG
"""

import inspect


def get_current_function_name():
    stack = inspect.stack()
    return stack[1].function  # stack[1][3]


class MyClass:
    def function_one(self):
        print("%s.%s invoked"%(self.__class__.__name__, get_current_function_name()))

if __name__ == "__main__":
    myclass = MyClass()
    myclass.function_one()
