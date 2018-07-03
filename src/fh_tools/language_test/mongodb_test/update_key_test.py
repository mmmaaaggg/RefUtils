# -*- coding: utf-8 -*-
"""
Created on 2017/7/6
@author: MG
"""

from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
try:
    db_name = 'test'
    db = client[db_name]
    collection_useraction = db['hello']
    # print(collection_useraction)
    old_key = {'p1': 'p123'}
    new_data = {'p1': 'p123', 'new_key': 'new value'}
    add_data = {'new_key': 'new value'}
    if collection_useraction.find_one(add_data) is not None:
        collection_useraction.remove(old_key)
    collection_useraction.insert_one(old_key.copy())
    if collection_useraction.update_one(old_key, {'$set': new_data}):
        result = collection_useraction.find_one(add_data)
        print("result['new_key'] == 'new value' ", result['new_key'] == 'new value')
finally:
    client.close()
