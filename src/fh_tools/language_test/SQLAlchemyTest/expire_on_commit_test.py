# -*- coding: utf-8 -*-
"""
Created on 2017/10/28
@author: MG
"""
from datetime import date, timedelta
from sqlalchemy import Column, Integer, Date, Float, String, Boolean, Time, create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
logger = logging.getLogger()

DB_INFO_DIC = {'type': 'mysql',
               'DB_IP': '10.0.3.66',
               'DB_PORT': '3306',
               'DB_NAME': 'qabat',
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

BaseModel = declarative_base()


class OrderInfo(BaseModel):
    """订单信息"""

    __tablename__ = 'order_info'
    order_id = Column(Integer, primary_key=True, autoincrement=True)
    stg_run_id = Column(Integer)
    # order_dt = Column(DateTime, server_default=func.now())
    order_date = Column(Date)  # 对应行情数据中 ActionDate
    order_time = Column(Time)  # 对应行情数据中 ActionTime
    order_millisec = Column(Integer)  # 对应行情数据中 ActionMillisec
    direction = Column(Boolean)  # 0：空；1：多
    action = Column(Integer)  # 0：关：1：开
    instrument_id = Column(String(30))
    order_price = Column(Float)
    order_vol = Column(Float)  # 订单量
    margin = Column(Float, server_default='0')  # 保证金 , comment="占用保证金"

    def __repr__(self):
        return "<OrderInfo(id='{0.order_id}', direction='{0.direction}', action='{0.action}', instrument_id='{0.instrument_id}', order_price='{0.order_price}', order_vol='{0.order_vol}')>".format(
            self)

order_info = OrderInfo(stg_run_id=1,
                       order_date=date.today(),
                       order_time=timedelta(minutes=1),
                       order_millisec=123,
                       direction=1,
                       action=1,
                       instrument_id='123',
                       order_price=123,
                       order_vol=123
                       )
engine = get_db_engine()
db_session = sessionmaker(bind=engine, expire_on_commit=False)
session = db_session()
try:
    session.add(order_info)
    # session.flush()
    session.commit()
finally:
    session.close()

# 更新成交信息
print("order_info.order_id", order_info.order_id)
