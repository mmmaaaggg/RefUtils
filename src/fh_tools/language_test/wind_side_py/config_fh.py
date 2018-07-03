from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from fh_tools import fh_utils, windy_utils_rest
from datetime import datetime
from redis import Redis
import logging

logger = logging.getLogger()

# 数据库地址 端口
DB_CONNECTION_DIC = {
    'dev_db': {'type': 'mysql',
               'DB_IP': '10.0.3.66',
               'DB_PORT': '3306',
               'DB_NAME': 'fof_ams_dev',
               'DB_USER': 'mg',
               'DB_PASSWORD': 'Abcd1234'
               },
    'fh_db': {'type': 'mysql',
              'DB_IP': '10.0.5.111',
              'DB_PORT': '3306',
              'DB_NAME': 'fof_ams_db',
              'DB_USER': 'mg',
              'DB_PASSWORD': 'Abcd1234'
              },
    'wangch_db': {'type': 'sqlite',
                  'URL': 'sqlite:///%s' % r'D:\Downloads\DBAccountingA.db'
                  }
}
JSON_DB = '{"DB_PORT":"3306","DB_NAME":"fof_ams_db","DB_PASSWORD":"Abcd1234","DB_USER":"mg","DB_IP":"10.0.5.111"}'
# 策略中英文名称对照关系
STRATEGY_EN_CN_DIC = {
    'long_only': '股票多头策略',
    'long_short': '股票多空策略',
    'event_driven': '事件驱动策略',
    'other_equity': '其他股票策略',
    'alpha': '阿尔法策略',
    'fixed_income': '债券策略',
    'money_market': '货币市场策略',
    'cta': '管理期货策略',
    'arbitrage': '套利策略',
    'macro': '宏观策略',
}
STRATEGY_CN_EN_DIC = {cn: en for en, cn in STRATEGY_EN_CN_DIC.items()}
# 模型静态文件缓存目录
ANALYSIS_CACHE_FILE_NAME = 'analysis_cache'
STR_FORMAT_DATE = '%Y-%m-%d'
UN_AVAILABLE_DATE = datetime.strptime('1900-01-01', STR_FORMAT_DATE).date()

# "http://10.0.3.84:5000/wind/"
WIND_REST_URL = "http://10.0.3.66:5000/wind/"  # "http://10.0.5.110:5000/wind/"

# 配置Redis数据库地址、端口、db
REDIS_DB_HOST = '10.0.5.107'
REDIS_DB_PORT = 6379
REDIS_DB_DB = 1

STRESS_TESTING_SIMULATE_COUNT_COPULA = 5000
STRESS_TESTING_SIMULATE_COUNT_FHS_GARCH = 1000


def get_db_engine(db_name='dev_db') -> object:  # fh_db dev_db
    """初始化数据库engine"""
    db_info_dic = DB_CONNECTION_DIC[db_name]
    if db_info_dic['type'] == 'mysql':
        engine = create_engine(
            "mysql://%(DB_USER)s:%(DB_PASSWORD)s@%(DB_IP)s:%(DB_PORT)s/%(DB_NAME)s?charset=utf8"
            % db_info_dic,  # dev_db fh_db
            echo=False, encoding="utf-8")
        # logger.debug('开始连接DB:{}'.format(db_name))
    elif db_info_dic['type'] == 'sqlite':
        engine = create_engine(db_info_dic['URL'], echo=False, encoding="utf-8")
    # logger.debug("{}数据库已连接".format(db_name))
    return engine


def get_wind_rest():
    rest = windy_utils_rest.WindRest(WIND_REST_URL)
    return rest


class session_wrapper:
    """用于对session对象进行封装，方便使用with语句进行close控制"""

    def __init__(self, session):
        self.session = session

    def __enter__(self) -> Session:
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
        # print("close session")


def get_db_session(engine=None):
    """创建session对象，返回 session_wrapper 可以使用with语句进行调用"""
    if engine is None:
        engine = get_db_engine()
    db_session = sessionmaker(bind=engine)
    session = db_session()
    return session_wrapper(session)


def get_cache_file_path(file_name):
    return fh_utils.get_cache_file_path(ANALYSIS_CACHE_FILE_NAME, file_name)


def get_redis(host=REDIS_DB_HOST, port=REDIS_DB_PORT, db=REDIS_DB_DB) -> Redis:
    """add default argv"""
    # logger.info("初始化redis数据库{} {} {}".format(host, port, db))
    r = Redis(host,port, db)
    # logger.info("redis连接成功")
    return r


if __name__ == '__main__':
    rest = get_wind_rest()
    ret_df = rest.wsd("000001.SH", "open,high,low,close,volume,amt", "2017-04-25", "2017-04-25", None)
    print(ret_df)
