#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/10/31 17:43
@File    : test_init_func.py
@contact : mmmaaaggg@163.com
@desc    : 
"""
from sqlalchemy import Column, Integer, String, create_engine, exc, orm, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from src.fh_tools.db_utils import get_db_session

Base = declarative_base()


def get_db_engine(db_name='test') -> object:
    """初始化数据库engine"""
    # 数据库地址 端口
    DB_IP = "localhost"  # '10.0.5.111'
    DB_PORT = "3306"
    # 数据库用户名
    DB_USER = "mg"
    # 数据库密码
    DB_PASSWORD = "Dcba1234"

    engine = create_engine("mysql://%s:%s@%s:%s/%s?charset=utf8" % (
        DB_USER, DB_PASSWORD, DB_IP, DB_PORT, db_name),
                           echo=False, encoding="utf-8")
    return engine


class User(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    fullname = Column(String(20))
    password = Column(String(40))

    def __init__(self, name, fullname):
        self.name = name
        self.fullname = fullname


def _test_only():
    engine = get_db_engine()
    Base.metadata.create_all(engine)

    session = get_db_session(engine)
    try:
        user = User('a', 'abc')
        session.add(user)
        session.commit()
    finally:
        session.close()


def _test_only2():
    engine = get_db_engine()
    Base.metadata.create_all(engine)

    session = get_db_session(engine)
    try:
        user = session.query(User).filter(User.id == 1).first()
        print(user)
    finally:
        session.close()


if __name__ == "__main__":
    # _test_only()
    _test_only2()
