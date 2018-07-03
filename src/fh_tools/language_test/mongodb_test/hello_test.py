# -*- coding: utf-8 -*-
"""
Created on 2017/6/14
@author: MG
"""
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
try:
    db_name = 'test'
    db = client[db_name]
    collection_useraction = db['hello']
    # print(collection_useraction)
    print('hello collection')
    for raw in collection_useraction.find().limit(5):
        print(raw)

    # no data will be insert
    # class A:
    #
    #     p1, p2 = 'p1', 2
    #
    # data = A()
    # print('insert data:', data.__dict__)
    # collection_useraction.insert_one(data.__dict__)
    collection_useraction.insert_one({'p1': 'p123'})
    for raw in collection_useraction.find({'p1': 'p1'}):
        print(raw)
    print("find_one({'p1': 'p123'})", collection_useraction.find_one({'p1': 'p123'}))
    collection_useraction.remove({'p1': 'p123'})
finally:
    client.close()
# order_collection = db.create_collection('hello')
# order_collection.insert({'afs': 123, 'bdf': 432})
# print('hello')
# for raw in order_collection.find():
#     print(raw)

