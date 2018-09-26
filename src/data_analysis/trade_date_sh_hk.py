#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/9/26 11:12
@File    : trade_date_sh_hk.py
@contact : mmmaaaggg@163.com
@desc    : 港交所、沪深交易所交易日对比
"""
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("mysql://mg:Dcba1234@localhost/md_integration?charset=utf8")

sql_str = """select hk '香港', sz '沪深' from
    (
        select hk.trade_date hk, sz.trade_date sz from 
        (
            select * from wind_trade_date where exch_code = 'HKEX'
        ) hk
        left outer join
        (
            select * from wind_trade_date where exch_code = 'SZSE'
        ) sz
        on hk.trade_date = sz.trade_date
        union
        select hk.trade_date hk, sz.trade_date sz from 
        (
            select trade_date from wind_trade_date where exch_code = 'HKEX'
        ) hk
        right outer join
        (
            select trade_date from wind_trade_date where exch_code = 'SZSE'
        ) sz
        on hk.trade_date = sz.trade_date
    ) merged
    where ifnull(hk, sz) between '2018-9-1' and '2018-10-10'
    order by ifnull(hk, sz)"""
data_df = pd.read_sql(sql_str, engine)
data_df.to_excel('trade_date_sh_hk.xls')
