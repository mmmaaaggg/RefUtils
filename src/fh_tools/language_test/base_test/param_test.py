# -*- coding: utf-8 -*-
"""
Created on 2017/4/23
@author: MG
"""


def func(a, b, *arg):
    print('func params:a="%s" ' % a, 'b="%s" ' % b, '*arg=', *arg)
params = ['a1', 'b1', 'c1', 'd1']
func(*params)


def func(a, b, **kwargs):
    print('func params:a="%s" ' % a, 'b="%s" ' % b, '*arg=', kwargs)
params = {'a': 'a1', 'b': 'b1', 'c': 'c1', 'd': 'd1'}
func(**params)
