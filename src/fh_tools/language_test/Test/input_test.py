#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/9/28 13:57
@File    : input_test.py
@contact : mmmaaaggg@163.com
@desc    : 
"""

import sys
import time
from select import select
timeout = 4
prompt ="Type any number from 0 up to 9"
default = 99


def input_with(prompt, timeout, default):
    """Read an input from the user or timeout"""
    print(prompt)
    sys.stdout.flush()
    rlist, _, _ = select([sys.stdin], [], [], timeout)
    if rlist:
        s = int(sys.stdin.read().replace('n',''))
    else:
        s = default
    print(s)
    return s


if __name__ == "__main__":
    input_with(prompt, timeout, default)
