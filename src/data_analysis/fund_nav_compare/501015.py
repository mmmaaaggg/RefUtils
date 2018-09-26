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

mpl.rcParams['font.sans-serif'] = ['SimHei']  # 字体可以根据需要改动
mpl.rcParams['axes.unicode_minus'] = False  # 解决中文减号不显示的问题
engine = create_engine("mysql://mg:Dcba1234@localhost/md_integration?charset=utf8")
data_df = pd.read_excel(r'D:\WSPych\RefUtils\src\data_analysis\fund_nav_compare\501015.xlsx').rename(
    columns={'日期': 'trade_date', '收盘价(元)': 'nav'})[['trade_date', 'nav']].set_index('trade_date')
index_code = '399102.SZ'
index_df = pd.read_sql("select trade_date, close from wind_index_daily where wind_code = %s", engine,
                       params=[index_code], index_col=['trade_date'])
merge_df = merge_df = data_df.merge(index_df, left_index=True, right_index=True, sort=True)
rr_df = (merge_df.pct_change().fillna(0) + 1).cumprod().rename(columns={'nav': '财通升级 501015',
                                                                        'close': index_code})
rr_df.plot(title='财通升级501015 与指数 %s 对比' % index_code)
plt.show()
