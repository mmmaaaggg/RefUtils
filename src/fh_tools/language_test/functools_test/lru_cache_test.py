# -*- coding: utf-8 -*-
"""
Created on 2017/9/30
@author: MG
"""
import functools
from src.fh_tools.language_test.functools_test.clockdeco2 import clock, Clocker
import time

# @functools.lru_cache()
# @clock
@Clocker()
def fibonacci(n):
    if n < 2:
        return n
    time.sleep(0.5)
    return  fibonacci(n-2) + fibonacci(n-1)

if __name__ == "__main__":
    print(fibonacci(6))
