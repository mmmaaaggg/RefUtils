# -*- coding: utf-8 -*-
"""
Created on 2017/12/12
@author: MG
"""
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


def task(param1, param2):
    print(param1)
    time.sleep(4)
    if param2 == "end2":
        raise ValueError("param2 error")
    print(param2)
    return param1 + ' -> ' + param2


with ThreadPoolExecutor(max_workers=2) as pool:
    result1 = pool.submit(task, "start1", "end1")
    result2 = pool.submit(task, "start2", "end2")
    result3 = pool.submit(task, "start3", "end3")
    result4 = pool.submit(task, "start4", "end4")
    for result in as_completed([result1, result2, result3, result4]):
        try:
            print(result.result())
        except ValueError as exp:
            print(exp.args)


print('all finished')
