# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 17:21:14 2017

@author: forise
"""

import pandas as pd
import numpy as np
import tushare as ts
from  multiprocessing import Pool,freeze_support
import datetime


def get_current_price(stks_in, filepath_in=None):
    subdata=ts.get_today_all()
    subdata.set_index('code',inplace=True)
    subdata=subdata[['settlement','trade','volume','amount']]
    subdata.columns=['pre_close','price','volume','amount']

    check_list=set(stks_in) - set(subdata.index)

    if len(check_list) > 0:
        check_data=pd.DataFrame(columns=['pre_close','price','volume','amount','code'])
        for stk in check_list:
            realtime = ts.get_realtime_quotes(stk)
            if realtime is not None:
                realtime = realtime[['pre_close','price','volume','amount','code']]
                check_data = check_data.append(realtime)
        check_data.set_index('code',inplace=True)
        subdata = subdata.append(check_data)
    # print('sdf')
    subdata = subdata.ix[stks_in]
    if filepath_in is None:
        return subdata
    else:
        subdata.to_csv(filepath_in)

def Test():
    startt = datetime.datetime.now()
    filepath = r'CurrentPriceZG.csv'
    #stocks = ts.get_stock_basics()
    stocks = ['300354',
            '300402',
            '300281',
            '300397',
            '300095',
            '300046',
            '300395',
            '002560',
            '002231',
            '300365',
            '300099',
            '002406',
            '002446',
            '002214',
            '300008',
            '002669',
            '300045',
            '002542',
            '000595',
            '601208',
            '002309',
            '002361',
            '603885',
            '300325',
            '002297',
            '002046',
            '002097',
            '000026',
            '600698',
            '300265',
            '600353',
            '002338',
            '002111',
            '300053',
            '002339',
            '002651',
            '002253',
            '600592'
             ]
    get_current_price(stocks,filepath)
    
    endt = datetime.datetime.now()
    print(endt-startt)
# Test()