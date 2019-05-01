#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 19-4-9 上午9:05
@File    : dynamic_load.py
@contact : mmmaaaggg@163.com
@desc    : 
"""


# from src.fh_tools.language_test.base_test.dynamic_import_demo.a_class import AClass


def createInstance1(module_name, class_name, *args, **kwargs):
    module_meta = __import__(module_name, globals(), locals(), [class_name])
    class_meta = getattr(module_meta, class_name)
    obj = class_meta(*args, **kwargs)
    return obj


def load_1():
    obj = createInstance1("src.fh_tools.language_test.base_test.dynamic_import_demo.a_class", "AClass", 'mg')
    obj.say_name()


def createInstance2(module_name, class_name, *args, **kwargs):
    import importlib
    module_meta = importlib.import_module(module_name)
    class_meta = getattr(module_meta, class_name)
    obj = class_meta(*args, **kwargs)
    return obj


def load_2():
    obj = createInstance1("src.fh_tools.language_test.base_test.dynamic_import_demo.a_class", "AClass", 'mg')
    obj.say_name()


if __name__ == "__main__":
    load_1()
    # load_2()
