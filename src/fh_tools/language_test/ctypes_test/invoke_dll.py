#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/3/22 9:41
@File    : invoke_dll.py
@contact : mmmaaaggg@163.com
@desc    : 
"""

from ctypes import *
dll_file_path = r"D:\WSVS\LanguageTest\x64\Debug\MyDll2.dll"
handle = cdll.LoadLibrary(dll_file_path)
# handle = oledll.LoadLibrary(dll_file_path)
# handle = windll.LoadLibrary(dll_file_path)
# handle = WinDLL(r"D:\WSVS\LanguageTest\Debug\MyDll.dll")

print('display()')
handle.display()
print('display(100)')
handle.display_int(100)

# handle.Add
# func.argtypes = (c_double,c_double)
# func.restype = c_double
# tmp = handle.Add(12,321)
# print(tmp)