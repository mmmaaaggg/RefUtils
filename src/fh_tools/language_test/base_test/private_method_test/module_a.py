# -*- coding: utf-8 -*-
"""
Created on 2017/6/22
@author: MG
"""


class A:
    __a = 'a value'

    def print(self):
        print(self.__a)

    def _print(self):
        print(self.__a)

    def __print(self):
        print(self.__a)