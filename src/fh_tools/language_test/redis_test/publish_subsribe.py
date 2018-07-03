# -*- coding: utf-8 -*-
"""
Created on 2017/7/16
@author: MG
"""

from redis import StrictRedis, ConnectionPool

conn_pool = ConnectionPool(host='192.168.159.131', port=6379, db=1)
r = StrictRedis(connection_pool=conn_pool)
pub_sub = r.pubsub()
print(type(pub_sub))
pub_sub.subscribe('pubsub_msg')
for item in pub_sub.listen():
    print(item)
    if item['data'] == b'over':
        break