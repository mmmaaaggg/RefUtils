# -*- coding: utf-8 -*-
"""
Created on 2017/7/7
@author: MG
"""
from sqlalchemy import create_engine, MetaData, Column, Integer, String, VARBINARY
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.schema import Table
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s: %(levelname)s [%(name)s] %(message)s')
logger = logging.getLogger()


#通过ConnectionPooling 连接数据库
# engine = create_engine("mysql+pymysql://root@127.0.0.1:3306/test", max_overflow=5,echo=True)
#通过Dialect执行SQL


DB_INFO_DIC = {'type': 'mysql',
               'DB_IP': '10.0.3.66',
               'DB_PORT': '3306',
               'DB_NAME': 'quant_db',
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


if __name__ == "__main__":
    # engine = create_engine('sqlite:///:memory:', echo=True)
    engine = get_db_engine()
    metadata = MetaData()
    #创建user表，继承metadata类
    #Engine使用Schama Type创建一个特定的结构对象
    testonly_tableobj = Table("testonly", metadata,
                              Column("id", Integer, primary_key=True),
                              Column("name", String(20)),
                              Column('bytes', VARBINARY(20))
                              )

    # color = Table("color", metadata,
    #               Column("id", Integer, primary_key=True),
    #               Column("name", String(20)))
    metadata.create_all(engine) #创建表结构

    conn =engine.connect()
    try:
        conn.execute(testonly_tableobj.insert(), {'id':2, "name": "koka", 'bytes': b'1234'})
        logger.info('insert data successfully')
        sql_str = testonly_tableobj.select()
        table_data = conn.execute(sql_str)
        for content in table_data.fetchall():
            logger.info('%s', content)
    finally:
        conn.close()
