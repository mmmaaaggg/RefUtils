# -*- coding: utf-8 -*-
"""
Created on 2017/5/2
@author: MG
"""
from src.fh_tools.language_test.wind_side_py.config_fh import STR_FORMAT_DATE, get_db_engine, get_db_session
from datetime import date, timedelta
from fh_tools import windy_utils
from fh_tools.windy_utils import wsd_cache, wsi_cache
from WindPy import w
import pandas as pd
from sqlalchemy.types import String, Date, Float, DateTime
from collections import OrderedDict


def df_to_sql(data_df_list):
    data_df_count = len(data_df_list)
    if data_df_count > 0:
        print('merge data with %d df' % data_df_count)
        data_df = pd.concat(data_df_list)
        data_df.dropna(inplace=True)
        data_df.index.rename('trade_datetime', inplace=True)
        data_df.reset_index(inplace=True)
        data_df['trade_date'] = data_df['trade_datetime'].apply(lambda x: x.date())
        data_df = data_df.set_index(['wind_code', 'trade_datetime'])
        # data_df.rename(columns={'oi': 'position'}, inplace=True)
        engine = get_db_engine()
        data_count = data_df.shape[0]
        data_df.to_sql('wind_future_minute', engine, if_exists='append',
                       index_label=['wind_code', 'trade_datetime'],
                       dtype={
                           'wind_code': String(20),
                           'trade_datetime': DateTime,
                           'trade_date': Date,
                           'open': Float,
                           'high': Float,
                           'low': Float,
                           'close': Float,
                           'volume': Float,
                           'amount': Float,
                           'position': Float,
                       })
        print('%d data import' % data_count)
    else:
        print('no data for merge')


def import_wind_future_munite():
    # w.wsd("AG1612.SHF", "open,high,low,close,volume,amt,dealnum,settle,oi,st_stock", "2016-11-01", "2016-12-21", "")
    sql_str = """select fi.wind_code, ifnull(trade_date_max_1, subdate(ipo_date, 1)) date_frm, 
if(subdate(curdate(), 1)<lasttrade_date,subdate(curdate(), 1),lasttrade_date) date_to
from wind_future_info fi left outer join
(select wind_code, adddate(max(trade_date),1) trade_date_max_1 from wind_future_minute group by wind_code) wfd
on fi.wind_code = wfd.wind_code
order by fi.wind_code desc"""
    engine = get_db_engine()
    future_date_dic = OrderedDict()
    with get_db_session(engine) as session:
        table = session.execute(sql_str)
        for wind_code, date_frm, date_to in table.fetchall():
            future_date_dic[wind_code] = (date_frm, date_to)
    data_df_list = []
    w.start()
    try:
        for wind_code, date_pair in future_date_dic.items():
            # if wind_code not in ('AU1703.SHF', 'AU1611.SHF'):
            #     continue
            date_frm, date_to = date_pair
            if date_to < date.today() - timedelta(1000):
                print('%s 三年以上历史分钟线数据无法获取' % wind_code)
                continue
            if date_frm >= date_to:
                continue
            date_frm_str = date_frm.strftime('%Y-%m-%d 20:59:00')
            date_to_str = date_to.strftime('%Y-%m-%d 15:00:00')
            print('get %s between %s and %s' % (wind_code, date_frm_str, date_to_str))
            data_df_tmp = wsi_cache(w, wind_code, "open,high,low,close,volume,amt,oi",
                                    date_frm_str, date_to_str, "")
            if data_df_tmp is None:
                continue
            data_df_tmp = data_df_tmp[data_df_tmp['volume'].apply(lambda x: x > 0)]
            if data_df_tmp.shape[0] == 0:
                print('%s has no available data' % wind_code)
                continue
            data_df_tmp['wind_code'] = wind_code
            data_df_list.append(data_df_tmp)
            if len(data_df_list) > 20:
                df_to_sql(data_df_list)
                data_df_list = []
    finally:
        df_to_sql(data_df_list)
        w.close()


if __name__ == "__main__":
    windy_utils.CACHE_ENABLE = False
    import_wind_future_munite()
