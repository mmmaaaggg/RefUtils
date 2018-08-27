#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/3/22 9:44
@File    : invoke_windll.py
@contact : mmmaaaggg@163.com
@desc    : 
"""

# 基本信息和使用printf
from ctypes import *  # @UnusedWildImport

print(windll.kernel32)

msvcrt = cdll.msvcrt
print("msvcrt", msvcrt)

print("msvcrt.printf", msvcrt.printf)
msg_str = b"Hello world!\n"
msvcrt.printf(b"Testing: %s", msg_str)
# 强制刷新缓冲区，立即输出，
# 若无此句，会导致下面的python语句输出结束了才输出下面的字符串
msvcrt.fflush(0)
