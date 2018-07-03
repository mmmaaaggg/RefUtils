# -*- coding: utf-8 -*-
"""
Created on 2017/5/2
@author: MG
"""
from datetime import datetime, date, timedelta
from src.fh_tools.language_test.wind_side_py.config_fh import STR_FORMAT_DATE, get_db_engine, get_db_session
from WindPy import w
from fh_tools.windy_utils import wset_cache, wss_cache
from fh_tools import windy_utils
from sqlalchemy.types import String, Date, Float
import re

RE_PATTERN_MFPRICE = re.compile(r'\d*\.*\d*')


def mfprice_2_num(input_str):
    m = RE_PATTERN_MFPRICE.search(input_str)
    if m is not None:
        return m.group()
    else:
        return 0


def get_date_since(wind_code_ipo_date_dic, regex_str, date_establish):
    """
    获取最新的合约日期，如果没有对应合约日期则返回该品种起始日期
    :param wind_code_ipo_date_dic: 
    :param regex_str: 
    :param date_establish: 
    :return: 
    """
    date_since = date_establish
    ndays_per_update = 60
    for wind_code, ipo_date in wind_code_ipo_date_dic.items():
        m = re.match(regex_str, wind_code)
        if m is not None and date_since < ipo_date:
            date_since = ipo_date
    # if date_since != date_establish:
    #     date_since += timedelta(days=ndays_per_update)
    return date_since


def import_wind_future_info():

    # 获取已存在合约列表
    sql_str = 'select wind_code, ipo_date from wind_future_info'
    engine = get_db_engine()
    with get_db_session(engine) as session:
        table = session.execute(sql_str)
        wind_code_ipo_date_dic = dict(table.fetchall())

    # 通过wind获取合约列表
    w.start()
    future_sectorid_dic_list = [
        {'subject_name': 'CFE 沪深300', 'regex': r"IF\d{4}\.CFE",
         'sectorid': 'a599010102000000', 'date_establish': '2010-4-16'},
        {'subject_name': 'CFE 上证50', 'regex': r"IH\d{4}\.CFE",
         'sectorid': '1000014871000000', 'date_establish': '2015-4-16'},
        {'subject_name': 'CFE 中证500', 'regex': r"IC\d{4}\.CFE",
         'sectorid': '1000014872000000', 'date_establish': '2015-4-16'},
        {'subject_name': 'SHFE 黄金', 'regex': r"AU\d{4}\.SHF",
         'sectorid': 'a599010205000000', 'date_establish': '2008-01-09'},
        {'subject_name': 'SHFE 沪银', 'regex': r"AG\d{4}\.SHF",
         'sectorid': '1000006502000000', 'date_establish': '2012-05-10'},
        {'subject_name': 'SHFE 螺纹钢', 'regex': r"RB\d{4}\.SHF",
         'sectorid': 'a599010206000000', 'date_establish': '2009-03-27'},
        {'subject_name': 'SHFE 热卷', 'regex': r"HC\d{4}\.SHF",
         'sectorid': '1000011455000000', 'date_establish': '2014-03-21'},
        {'subject_name': 'DCE 焦炭', 'regex': r"J\d{4}\.SHF",
         'sectorid': '1000002976000000', 'date_establish': '2011-04-15'},
        {'subject_name': 'DCE 焦煤', 'regex': r"JM\d{4}\.SHF",
         'sectorid': '1000009338000000', 'date_establish': '2013-03-22'},
        {'subject_name': '铁矿石', 'regex': r"I\d{4}\.SHF",
         'sectorid': '1000006502000000', 'date_establish': '2013-10-18'},
        {'subject_name': '铅', 'regex': r"PB\d{4}\.SHF",
         'sectorid': '1000002892000000', 'date_establish': '2011-3-24'},
    ]
    wind_code_set = set()
    ndays_per_update = 60
    # 获取历史期货合约列表信息
    for future_sectorid_dic in future_sectorid_dic_list:
        subject_name = future_sectorid_dic['subject_name']
        sector_id = future_sectorid_dic['sectorid']
        regex_str = future_sectorid_dic['regex']
        date_establish = datetime.strptime(future_sectorid_dic['date_establish'], STR_FORMAT_DATE).date()
        date_since = get_date_since(wind_code_ipo_date_dic, regex_str, date_establish)
        date_yestoday = date.today() - timedelta(days=1)
        while date_since <= date_yestoday:
            date_since_str = date_since.strftime(STR_FORMAT_DATE)
            # w.wset("sectorconstituent","date=2017-05-02;sectorid=a599010205000000")
            future_info_df = wset_cache(w, "sectorconstituent", "date=%s;sectorid=%s" % (date_since_str, sector_id))
            wind_code_set |= set(future_info_df['wind_code'])
            # future_info_df = future_info_df[['wind_code', 'sec_name']]
            # future_info_dic_list = future_info_df.to_dict(orient='records')
            # for future_info_dic in future_info_dic_list:
            #     wind_code = future_info_dic['wind_code']
            #     if wind_code not in wind_code_future_info_dic:
            #         wind_code_future_info_dic[wind_code] = future_info_dic
            if date_since >= date_yestoday:
                break
            else:
                date_since += timedelta(days=ndays_per_update)
                if date_since > date_yestoday:
                    date_since = date_yestoday
    # 获取合约列表
    wind_code_list = [wc for wc in wind_code_set if wc not in wind_code_ipo_date_dic]
    # 获取合约基本信息
    # w.wss("AU1706.SHF,AG1612.SHF,AU0806.SHF", "ipo_date,sec_name,sec_englishname,exch_eng,lasttrade_date,lastdelivery_date,dlmonth,lprice,sccode,margin,punit,changelt,mfprice,contractmultiplier,ftmargins,trade_code")
    future_info_df = wss_cache(w, wind_code_list,
                               "ipo_date,sec_name,sec_englishname,exch_eng,lasttrade_date,lastdelivery_date,dlmonth,lprice,sccode,margin,punit,changelt,mfprice,contractmultiplier,ftmargins,trade_code,thours")

    future_info_df['MFPRICE'] = future_info_df['MFPRICE'].apply(mfprice_2_num)
    future_info_count = future_info_df.shape[0]

    future_info_df.rename(columns={c: str.lower(c) for c in future_info_df.columns}, inplace=True)
    future_info_df.index.rename('wind_code', inplace=True)
    future_info_df.to_sql('wind_future_info', engine, if_exists='append',
                          dtype={
                              'wind_code': String(20),
                              'trade_code': String(20),
                              'sec_name': String(50),
                              'sec_englishname': String(50),
                              'exch_eng': String(50),
                              'ipo_date': Date,
                              'lasttrade_date': Date,
                              'lastdelivery_date': Date,
                              'dlmonth': String(20),
                              'lprice': Float,
                              'sccode': String(20),
                              'margin': Float,
                              'punit': String(20),
                              'changelt': Float,
                              'mfprice': Float,
                              'contractmultiplier': Float,
                              'ftmargins': String(100),
                              'thours': String(200),
                          })
    print('%d data import' % future_info_count)
    w.close()


if __name__ == "__main__":
    windy_utils.CACHE_ENABLE = False
    import_wind_future_info()
