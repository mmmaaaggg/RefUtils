# -*- coding: utf-8 -*-
"""
Created on 2017/4/25
@author: MG
"""

import redis

r = redis.Redis(host='192.168.159.131', port=6379, db=1)
name = 'some set name'
value1 = 'value1'
r.set(name, value1)
value2 = 'value2'
print(r.getset(name, value2)) #输出: value1
print(r.get(name)) #输出:value2
