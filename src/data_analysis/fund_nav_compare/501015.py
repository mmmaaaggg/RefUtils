#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/9/25 17:27
@File    : 501015.py
@contact : mmmaaaggg@163.com
@desc    : 
"""
import matplotlib.pyplot as plt
from pylab import mpl
import pandas as pd
from sqlalchemy import create_engine
from src.fh_tools.db_utils import with_db_session
from datetime import datetime

mpl.rcParams['font.sans-serif'] = ['SimHei']  # 字体可以根据需要改动
mpl.rcParams['axes.unicode_minus'] = False  # 解决中文减号不显示的问题
engine = create_engine("mysql://mg:Dcba1234@localhost/md_integration?charset=utf8")
# data_df = pd.read_excel(r'D:\WSPych\RefUtils\src\data_analysis\fund_nav_compare\501015 close.xlsx').rename(
#     columns={'日期': 'trade_date', '收盘价(元)': 'nav'})[['trade_date', 'nav']].set_index('trade_date')
data_df = pd.read_excel(r'D:\WSPych\RefUtils\src\data_analysis\fund_nav_compare\501015 nav.xlsx').rename(
    columns={'日期': 'trade_date', '501015': 'nav'})[['trade_date', 'nav']]
data_df['trade_date'] = data_df['trade_date'].apply(lambda x: x.date() if isinstance(x, datetime) else None)
data_df.set_index('trade_date', inplace=True)
index_code = '000300.SH'  # '399102.SZ'
with with_db_session(engine) as session:
    index_name = session.execute(
        'SELECT sec_name FROM wind_index_info WHERE wind_code=:wind_code',
        params={'wind_code': index_code}).scalar()
sec_name = index_name + " " + index_code
index_df = pd.read_sql("SELECT trade_date, close FROM wind_index_daily WHERE wind_code = %s", engine,
                       params=[index_code], index_col=['trade_date'])
merge_df = data_df.merge(index_df, left_index=True, right_index=True, sort=True)
merge_df[sec_name] = (merge_df['close'].pct_change().fillna(0) + 1).cumprod()
rr_df = merge_df[['nav', sec_name]].rename(columns={'nav': '财通升级 501015'})
rr_df.plot(title='财通升级501015 与指数 %s 对比' % index_code)
plt.show()
rr_df.to_excel('财通升级501015 与指数 %s 对比.xls' % index_code)
