# -*- coding: utf-8 -*-
"""
Created on 2017/4/5
@author: MG
"""
from sqlalchemy import create_engine
import pandas as pd
import tushare as ts

# 数据库地址 端口
DB_IP = "10.0.3.66"
DB_PORT = "3306"
# 数据库名称
DB_NAME = "fof_ams_dev"
# 数据库用户名
DB_USER = "mg"
# 数据库密码
DB_PASSWORD = "Abcd1234"

engine = engine = create_engine("mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8" % (
    DB_USER, DB_PASSWORD, DB_IP, DB_PORT, DB_NAME),
                                echo=False, encoding="utf-8")
df = pd.read_sql("select * from index_tradeinfo where index_code=%s",
                 engine,
                 params=['000300.SH'])
print(df.head())
