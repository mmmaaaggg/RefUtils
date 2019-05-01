#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 19-4-9 上午9:03
@File    : a_class.py
@contact : mmmaaaggg@163.com
@desc    : 
"""


class AClass:
    def __init__(self, name):
        self.name = name

    def say_name(self):
        print('name is ', self.name)


def get_module_and_class_name():
    AClass.name


if __name__ == "__main__":
    aaa = AClass('mg')
    aaa.say_name()
