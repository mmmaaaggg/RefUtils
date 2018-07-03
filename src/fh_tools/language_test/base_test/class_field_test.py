# -*- coding: utf-8 -*-
"""
Created on 2017/6/18
@author: MG
"""
from collections import OrderedDict

class ClassFoo(object):
    def __init__(self):
        self.field1 = 1
        self.field2 = '2'
        self.field3 = '3'
        self.field4 = 4

    def print_c(self):
        print(self.__dict__)

cf = ClassFoo()
cf.print_c()
