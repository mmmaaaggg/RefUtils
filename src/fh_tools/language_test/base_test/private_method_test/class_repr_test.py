# -*- coding: utf-8 -*-
"""
Created on 2017/6/23
@author: MG
"""

class A:

    def __repr__(self):
        return "repr A"

    def __str__(self):
        return "str A"

aaa = A()

print("print(aaa):", aaa)
print("'%s' % aaa:", '%s' % aaa)
print("'%r' % aaa:", '%r' % aaa)
