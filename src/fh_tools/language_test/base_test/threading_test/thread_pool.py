# -*- coding: utf-8 -*-
"""
Created on 2017/7/19
@author: MG
"""
from threadpool import ThreadPool, makeRequests  # 此方法已经不推荐使用
import time


def sayhello(str):
    print("Hello ",str)
    time.sleep(2)

name_list =['xiaozi','aa','bb','cc']
poolsize = 10
pool = ThreadPool(poolsize)
requests = makeRequests(sayhello, name_list)
[pool.putRequest(req) for req in requests]
pool.wait()
