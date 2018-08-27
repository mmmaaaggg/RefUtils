#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/8/21 10:49
@File    : tushare_pro_blockchain.py
@contact : mmmaaaggg@163.com
@desc    : 
"""

import tushare as ts


TOKEN = "68729e7d0468c4ee8fe073c11ba748700ef1812f8e2dfe34117535d9"
ts.set_token(TOKEN)
pro = ts.pro_api()

# 交易所基本信息
# 获取所在地区为美国的交易所
exch_df = pro.coinexchanges(area='us')
# 按交易对数量排序
exch_df = exch_df.sort('pairs', ascending=False)

# 交易币基本信息
coinlist_df = pro.coinlist(start_date='20170101', end_date='20171231')

# 交易对数据
coinpair_df = pro.coinpair(exchange='huobi', trade_date='20180802')

# 行情数据
coinbar_df3 = pro.coinbar(exchange='huobi', symbol='e', freq='1min', start_date='20180701', end_date='20180801')


# df = pro.trade_cal(exchange_id='', start_date='20180101', end_date='', fields='pretrade_date', is_open='0')
df = pro.query('trade_cal', exchange_id='', start_date='20180101', end_date='', fields='pretrade_date', is_open='0')
