#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/3/21 17:59
@File    : example_build.py.py
@contact : mmmaaaggg@163.com
@desc    : 
"""

from cffi import FFI

ffibuilder = FFI()
ffibuilder.set_source("_simple_example", None)
ffibuilder.cdef("""
    int printf(const char *format, ...);
""")

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)