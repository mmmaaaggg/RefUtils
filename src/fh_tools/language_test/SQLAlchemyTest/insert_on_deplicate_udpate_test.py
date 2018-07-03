# -*- coding: utf-8 -*-
"""
Created on 2017/12/26
@author: MG
"""
import logging
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy import Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import Insert
from sqlalchemy.exc import IntegrityError


@compiles(Insert)
def append_string(insert, compiler, **kw):
    s = compiler.visit_insert(insert, **kw)
    if insert.kwargs.get('on_duplicate_key_update'):
        fields = s[s.find("(") + 1:s.find(")")].replace(" ", "").split(",")
        generated_directive = ["{0}=VALUES({0})".format(field) for field in fields]
        return s + " ON DUPLICATE KEY UPDATE " + ",".join(generated_directive)
    return s


logger = logging.getLogger()

DB_INFO_DIC = {'type': 'mysql',
               'DB_IP': '10.0.3.66',
               'DB_PORT': '3306',
               'DB_NAME': 'future_md_test',
               'DB_USER': 'mg',
               'DB_PASSWORD': 'Abcd1234'
               }


def get_db_engine() -> Engine:
    """初始化数据库engine"""

    if DB_INFO_DIC['type'] == 'mysql':
        engine = create_engine(
            "mysql+pymysql://%(DB_USER)s:%(DB_PASSWORD)s@%(DB_IP)s:%(DB_PORT)s/%(DB_NAME)s?charset=utf8"
            % DB_INFO_DIC,  # dev_db fh_db
            echo=False, encoding="utf-8")
        logger.debug('开始连接DB: %s', DB_INFO_DIC['DB_IP'])
    elif DB_INFO_DIC['type'] == 'sqlite':
        engine = create_engine(DB_INFO_DIC['URL'], echo=False, encoding="utf-8")
    else:
        raise ValueError("DB_INFO_DIC['type']=%s", DB_INFO_DIC['type'])
    logger.debug("数据库已连接")
    return engine


md_k_dic = {'UpdateTime': '14:43:00', 'high': 33333, 'PreClosePrice': 140750.0, 'shift_min': 0,
            'ActionTime': '14:43:36', 'InstrumentID': 'sn1807', 'open': 140750.0, 'PreSettlementPrice': 140750.0,
            'OpenInterest': 0.0, 'vol': 0, 'close': 140750.0, 'period_min': 15, 'Turnover': 0.0, 'OpenPrice': 0.0,
            'AveragePrice': 0.0, 'low': 140750.0, 'amount': 0.0, 'ExchangeInstID': '', 'PreOpenInterest': 0.0,
            'ActionDay': '2017-12-25', 'Volume': 0, 'ActionDateTime': '2017-12-25 14:54:00', 'ExchangeID': '',
            'LowerLimitPrice': 132300.0, 'LowestPrice': 0.0, 'HighestPrice': 0.0, 'UpperLimitPrice': 149190.0,
            'TradingDay': '2017-12-25'}
md_k_dic2 = {'UpdateTime': '14:43:00', 'high': 44444, 'PreClosePrice': 140750.0, 'shift_min': 0,
             'ActionTime': '14:43:36', 'InstrumentID': 'sn1807', 'open': 140750.0, 'PreSettlementPrice': 140750.0,
             'OpenInterest': 0.0, 'vol': 0, 'close': 140750.0, 'period_min': 15, 'Turnover': 0.0, 'OpenPrice': 0.0,
             'AveragePrice': 0.0, 'low': 140750.0, 'amount': 0.0, 'ExchangeInstID': '', 'PreOpenInterest': 0.0,
             'ActionDay': '2017-12-25', 'Volume': 0, 'ActionDateTime': '2017-12-25 14:54:00', 'ExchangeID': '',
             'LowerLimitPrice': 132300.0, 'LowestPrice': 0.0, 'HighestPrice': 0.0, 'UpperLimitPrice': 149190.0,
             'TradingDay': '2017-12-25'}

engine = get_db_engine()
BaseModel = declarative_base()
md_orm_table = Table('md_min_n', MetaData(engine), autoload=True)
db_session = sessionmaker(bind=engine, expire_on_commit=False)
session = db_session()
try:
    try:
        session.execute(
            "delete from md_min_n where InstrumentID=:InstrumentID and TradingDay=:TradingDay and UpdateTime=:UpdateTime and period_min=:period_min and shift_min=:shift_min",
            md_k_dic)
        session.execute(md_orm_table.insert(), md_k_dic)
        high = session.execute(
            "select high from md_min_n where InstrumentID=:InstrumentID and TradingDay=:TradingDay and UpdateTime=:UpdateTime and period_min=:period_min and shift_min=:shift_min",
            md_k_dic).first()[0]
        assert high, 33333
    except Exception as IntegrityError:
        pass

    session.execute(md_orm_table.insert(on_duplicate_key_update=True), md_k_dic2)
    high2 = session.execute(
        "select high from md_min_n where InstrumentID=:InstrumentID and TradingDay=:TradingDay and UpdateTime=:UpdateTime and period_min=:period_min and shift_min=:shift_min",
        md_k_dic).first()[0]
    assert high2, 44444
    # session.flush()
    # session.commit()
finally:
    session.close()
