# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 10:52:30 2017

@author: Yupeng Guo - alanguoyupeng@163.com

"""
import pandas as pd
from math import isnan
from WindPy import w
import pymysql
from sqlalchemy import create_engine
from fh_tools.windy_utils import wset_cache, wsd_cache, dump_cache
from datetime import datetime, date
# from API import connect_fh_db
from sqlalchemy.types import String, Date, Float
from pandas.tslib import Timestamp
from config_fh import get_db_engine, get_db_session


def import_smfund_daily():
    w.start()
    today = date.today().strftime('%Y-%m-%d')
    engine = get_db_engine()

    sql_str = """select wind_code, ifnull(trade_date_max, fund_setupdate) date_start, class_a_code, class_b_code
    from wind_smfund_info fi left outer join
    (select code_p, adddate(max(trade_date), 1) trade_date_max from wind_smfund_daily group by code_p) smd
    on fi.wind_code = smd.code_p
    where fund_setupdate is not null
    and class_a_code is not null
    and class_b_code is not null"""
    df = pd.read_sql(sql_str, engine)
    df.set_index('wind_code', inplace=True)

    df_count = df.shape[0]
    print('df_count', df_count)
    index_start = 0
    for i, code in enumerate(df.index):  # 可调整 # [100:min([df_count, 200])]
        if i < index_start:
            continue
        print('%d/%d) %s start to import' % (i, df_count, code))
        if type(df.loc[code, 'date_start']) not in (date, datetime, Timestamp):
            print('%d %s has no fund_setupdate will be ignored' % (i, code))
            # print(df.iloc[i, :])
            continue
        beginTime = df.loc[code, 'date_start'].strftime('%Y-%m-%d')
        field = "open,high,low,close,volume,amt,pct_chg"
        df_p = wsd_cache(w, code, field, beginTime, today, "")
        df_p.rename(columns=lambda x: x.swapcase(), inplace=True)
        df_p['code_p'] = code
        code_a = df.loc[code, 'class_a_code']
        if code_a is None:
            print('%d %s has no code_a will be ignored' % (i, code))
            # print(df.iloc[i, :])
            continue
        df_a = wsd_cache(w, code_a, field, beginTime, today, "")
        df_a.rename(columns=lambda x: x.swapcase() + '_a', inplace=True)
        code_b = df.loc[code, 'class_b_code']
        df_b = wsd_cache(w, code_b, field, beginTime, today, "")
        df_b.columns = df_b.columns.map(lambda x: x.swapcase() + '_b')
        new_df = pd.DataFrame()
        for d in df_p.index:
            time = d.date().strftime('%Y-%m-%d')
            field = "date=%s;windcode=%s;field=a_nav,b_nav,a_fs_inc,b_fs_inc,cur_interest,next_interest,tm_type,ptm_year,anal_pricelever,anal_navlevel,t1_premium,t2_premium,next_pcvdate,dq_status" % (
            time, code)
            temp = wset_cache(w, "leveragedfundinfo", field)
            temp['date'] = d
            new_df = new_df.append(temp)
        new_df['next_pcvdate'] = new_df['next_pcvdate'].map(lambda x: x.date() if x is not None else x)
        new_df.set_index('date', inplace=True)
        one_df = pd.concat([df_p, df_a, df_b, new_df], axis=1)
        one_df.reset_index(inplace=True)
        #    one_df['date'] = one_df['date'].map(lambda x: x.date())
        one_df.rename(columns={'date': 'trade_date'}, inplace=True)
        one_df.set_index(['code_p', 'trade_date'], inplace=True)
        one_df.to_sql('wind_smfund_daily', engine, if_exists='append', index_label=['code_p', 'trade_date'],
                      dtype={
                          'code_p': String(20),
                          'trade_date': Date,
                          'next_pcvdate': Date,
                          'a_nav': Float,
                          'b_nav': Float,
                          'a_fs_inc': Float,
                          'b_fs_inc': Float,
                          'cur_interest': Float,
                          'next_interest': Float,
                          'ptm_year': Float,
                          'anal_pricelever': Float,
                          'anal_navlevel': Float,
                          't1_premium': Float,
                          't2_premium': Float,
                          'dq_status': String(50),
                          'open': Float, 'high': Float, 'low': Float, 'close': Float,
                          'volume': Float, 'amt': Float, 'pct_chg': Float,
                          'open_a': Float, 'high_a': Float, 'low_a': Float, 'close_a': Float,
                          'volume_a': Float, 'amt_a': Float, 'pct_chg_a': Float,
                          'open_b': Float, 'high_b': Float, 'low_b': Float, 'close_b': Float,
                          'volume_b': Float, 'amt_b': Float, 'pct_chg_b': Float,
                      })
        print('%d/%d) %s import success' % (i, df_count, code))
    # info_df = info_df.append(one_df)
    # dump_cache()

if __name__ == "__main__":
    import_smfund_daily()
