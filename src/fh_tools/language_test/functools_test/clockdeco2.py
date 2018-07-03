# -*- coding: utf-8 -*-
"""
Created on 2017/9/30
@author: MG
"""

import time
import functools
DEFAULT_FMT = '[{elapsed:0.8f}s] {name}({args}) -> {result}'


def clock(func):
    @functools.wraps(func)
    def clocked(*args, **kwargs):
        t0 = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - t0
        name = func.__name__
        arg_lst = []
        if args:
            arg_lst.append(', '.join(repr(arg) for arg in args))
        if kwargs:
            pairs = ['%s=%r' % (k, w) for k, w in sorted(kwargs.items())]
            arg_lst.append(', '.join(pairs))
        arg_str = ', '.join(arg_lst)
        print('[%0.8fs] %s(%s) -> %r ' % (elapsed, name, arg_str, result))
        return result
    return clocked


def Clocker(fmt=DEFAULT_FMT):
    def decorate(func):
        name = func.__name__
        print('init clock for %s' % name)
        elapsed = 0

        @functools.wraps(func)
        def clocked(*args, **kwargs):
            nonlocal elapsed, name
            t0 = time.time()
            result = func(*args, **kwargs)
            elapsed += time.time() - t0
            arg_lst = []
            if args:
                arg_lst.append(', '.join(repr(arg) for arg in args))
            if kwargs:
                pairs = ['%s=%r' % (k, w) for k, w in sorted(kwargs.items())]
                arg_lst.append(', '.join(pairs))
            arg_str = ', '.join(arg_lst)
            # print('[%0.8fs] %s(%s) -> %r ' % (elapsed, name, arg_str, result))
            print(fmt.format(**locals()))
            return result

        return clocked
    return decorate
