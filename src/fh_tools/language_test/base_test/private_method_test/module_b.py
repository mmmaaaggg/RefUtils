# -*- coding: utf-8 -*-
"""
Created on 2017/6/22
@author: MG
"""

from src.fh_tools.language_test.base_test.private_method_test.module_a import A

a_obj = A()
print('a_obj.print()')
a_obj.print()

print('a_obj._print()')
a_obj._print()

try:
    a_obj.__print()
except Exception as exp:
    print('call a_obj.__print() cause exception', exp)
