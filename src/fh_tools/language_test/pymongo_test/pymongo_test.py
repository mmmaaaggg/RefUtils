# -*- coding: utf-8 -*-
"""
Created on 2017/5/12
@author: MG
"""

from pymongo import MongoClient, ASCENDING
client = MongoClient('localhost', 27017)
db = client.test
print(db.name)
print(db.my_collection)
db.my_collection.insert_one({"x": 10}).inserted_id
db.my_collection.insert_one({"x": 8}).inserted_id
db.my_collection.insert_one({"x": 11}).inserted_id
db.my_collection.find_one()

for item in db.my_collection.find():
    print(item["x"])

db.my_collection.create_index("x")
for item in db.my_collection.find().sort("x", ASCENDING):
    print(item["x"])

print([item["x"] for item in db.my_collection.find().limit(2).skip(1)])
