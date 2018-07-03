#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/3/21 18:13
@File    : simple_example.py
@contact : mmmaaaggg@163.com
@desc    : 
"""

from cffi import FFI
ffi = FFI()
# ffi.cdef("""int printf(const char *format, ...);   // copy-pasted from the man page""")
ffi.cdef("void say_hello();")
# C = ffi.dlopen(r"D:\WSVS\LanguageTest\Debug\LanguageTest.dll")
C = ffi.dlopen(r"LanguageTest.dll")
C.say_hello()
# arg = ffi.new(b"char[]", "world")         # equivalent to C code: char arg[] = "world";
# C.printf("hi there, %s.\n", arg)         # call printf