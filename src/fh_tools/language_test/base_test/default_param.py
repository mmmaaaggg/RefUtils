# -*- coding: utf-8 -*-
"""
Created on 2017/6/18
@author: MG
"""


def get_id():
    print('call get_id')
    return 10


def print_id(id=get_id()):
    print('id:%d' % id)

print('default')
print_id()

print('with param')
print_id(5)

print('default again')
print_id()

