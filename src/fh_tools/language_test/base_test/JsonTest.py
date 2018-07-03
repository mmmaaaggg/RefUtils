# -*- coding:utf-8 -*-
'''
Created on 2017年1月6日

@author: Family
'''
import json 
 
info = {'1MinLoad': 5, 'MemUse': '5G', 'DiskUse': '80G'} 
 
print('dumps 操作之前数据类型: %s' % type(info))
JsonInfo = json.dumps(info) 
print(JsonInfo) 
# dumps 将数据通过特殊的形式转换为所有程序语言都识别的字符串 
print('dumps 操作之后数据类型: %s' % type(JsonInfo))
 
# loads 将字符串通过特殊的形式转为python是数据类型  (将字符串转为字典) 
NewInfo = json.loads(JsonInfo) 
print('loads 操作之后数据类型为: %s' % type(NewInfo))
 
print('分割线'.center(50, '-'))
 
# dump 将数据通过特殊的形式转换为所有语言都识别的字符串并写入文件 
with open('SystemInfo.txt', 'w') as f: 
    json.dump(info, f) 
    print('dump file end!!') 
 
# load 从文件读取字符串并转换为python的数据类型 
with open('SystemInfo.txt', 'r') as f: 
    LoadInfo = json.load(f) 
    print('load file end, data type is %s' % type(LoadInfo), LoadInfo)

print('-'*20)
info = {'expectations': {'annual_return': 0, 'cvar': 0, 'volatility': 0.15},
        'strategies': ['alpha', 'arbitrage', 'cta'],
        'subjective_views': [{"strategy1": 'alpha', "strategy2": 'arbitrage', "value": 0.05}]
        }
JsonInfo = json.dumps(info)
print("策略投资组合优化")
print(JsonInfo)
info = {'expectations': {'annual_return': 0, 'cvar': 0, 'volatility': 0.15},
        'strategies': [{'strategy': 'alpha', 'percent': 50}, {'strategy': 'arbitrage', 'percent': 30}, {'strategy': 'cta', 'percent': 20}],
        'funds': [
            {'fund': 'J11039.OF', 'strategies': [{'strategy': 'alpha', 'percent': 50}, {'strategy': 'arbitrage', 'percent': 30}, {'strategy': 'cta', 'percent': 20}]},
            {'fund': 'J12092.OF', 'strategies': [{'strategy': 'alpha', 'percent': 20}, {'strategy': 'arbitrage', 'percent': 80}]},
            {'fund': 'J12118.OF', 'strategies': [{'strategy': 'alpha', 'percent': 30}, {'strategy': 'arbitrage', 'percent': 70}]},
            {'fund': 'J13440.OF', 'strategies': [{'strategy': 'alpha', 'percent': 60}, {'strategy': 'cta', 'percent': 40}]},
                  ],
        'subjective_views': [{"strategy1": 'alpha', "strategy2": 'arbitrage', "value": 0.05}],
        }
JsonInfo = json.dumps(info)
print("子基金投资组合优化")
print(JsonInfo)
info = {
        'expectations': {'annual_return': 0, 'cvar': 0, 'volatility': 0.15},
        'funds': [
            {'fund': 'J11039.OF', 'strategies': [{'strategy': 'alpha', 'percent': 50}, {'strategy': 'arbitrage', 'percent': 30}, {'strategy': 'cta', 'percent': 20}]},
            {'fund': 'J12092.OF', 'strategies': [{'strategy': 'alpha', 'percent': 20}, {'strategy': 'arbitrage', 'percent': 80}]},
            {'fund': 'J12118.OF', 'strategies': [{'strategy': 'alpha', 'percent': 30}, {'strategy': 'arbitrage', 'percent': 70}]},
            {'fund': 'J13440.OF', 'strategies': [{'strategy': 'alpha', 'percent': 60}, {'strategy': 'cta', 'percent': 40}]},
                  ],
        'subjective_views': [{"strategy1": 'alpha', "strategy2": 'arbitrage', "value": 0.05}],
        'strategies': [
            {'strategy': 'alpha', 'operator': 'largerorequal', 'percent': 50},
            {'strategy': 'arbitrage', 'operator': 'smallerorequal', 'percent': 30},
            {'strategy': 'cta', 'operator': 'smallerorequal', 'percent': 20}],
        }

JsonInfo = json.dumps(info)
print("子基金投资组合优化2")
print(JsonInfo)

info = {
        'DB_IP': "10.0.3.66",
        'DB_PORT': "3306",
        'DB_NAME': "fof_ams_dev",
        'DB_USER': "mg",
        'DB_PASSWORD': "Abcd1234",
        }
JsonInfo = json.dumps(info)
print("数据库链接")
print(JsonInfo)

# info = {'table_name': 'sectorconstituent', 'options': 'date=2017-03-21;sectorid=1000023121000000'}
info = {'options': 'date=2017-03-27;sectorid=1000023126000000', 'table_name': 'sectorconstituent'}
JsonInfo = json.dumps(info)
print("rest str")
print(JsonInfo)
