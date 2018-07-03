# -*- coding: utf-8 -*-
"""
Created on 2017/7/6
@author: MG
"""

aaa = {n + n: str(n) + '+' + str(n) for n in range(10)}

for n, (key, val) in enumerate(aaa.items()):

    print(n, key, val)
