#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/3/21 18:03
@File    : example.py.py
@contact : mmmaaaggg@163.com
@desc    : 
"""

from src.fh_tools.language_test.cffi_test._simple_example import ffi

# lib = ffi.dlopen(None)      # Unix: open the standard C library
import ctypes.util         # or, try this on Windows:
lib = ffi.dlopen(ctypes.util.find_library("c"))

lib.printf(b"hi there, number %d\n", ffi.cast("int", 2))
