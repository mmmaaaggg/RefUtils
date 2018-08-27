#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/8/26 16:44
@File    : CallbackTest.py
@contact : mmmaaaggg@163.com
@desc    : 
"""
from ctypes import *

dll_file_path = r"d:\WSVS\LanguageTest\x64\Debug\CallbackTest.dll"
handle = cdll.LoadLibrary(dll_file_path)
ret = handle.CCallbackTestApp.StaticCall(1)
