from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fh_tools import fh_utils
import pandas as pd

# 数据库地址 端口
DB_IP = "10.0.3.66"  # '10.0.5.111'
DB_PORT = "3306"
# 数据库名称
DB_NAME = "fof_ams_dev"  # "fof_ams_db"
# 数据库用户名
DB_USER = "mg"
# 数据库密码
DB_PASSWORD = "Abcd1234"


def get_db_engine() -> object:
    """初始化数据库engine"""

    engine = create_engine("mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8" % (
        DB_USER, DB_PASSWORD, DB_IP, DB_PORT, DB_NAME),
                           echo=False, encoding="utf-8")
    return engine


class session_wrapper:
    """用于对session对象进行封装，方便使用with语句进行close控制"""

    def __init__(self, session):
        self.session = session

    def __enter__(self):
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
        print('session closed')


def get_db_session(engine=None):
    """创建session对象，返回 session_wrapper 可以使用with语句进行调用"""
    if engine is None:
        engine = get_db_engine()
    db_session = sessionmaker(bind=engine)
    session = db_session()
    print('sesstion created')
    return session_wrapper(session)


if __name__ == '__main__':
    with get_db_session() as session:
        strategy_name = 'long_only'
        stg_table = session.execute(
            'SELECT nav_date_week, wind_code_str, sample_name FROM strategy_index_info where strategy_name=:stg_name order by nav_date_week desc',
            {'stg_name': strategy_name})
        date_last = None
        index_pct_s = None
        sample_name_list = []
        sample_val_list = []
        stg_table_data_list = []
        for stg_info in stg_table.fetchall():
            # date_since = stg_info[0]
            # wind_code_str = stg_info[1]
            sample_name = stg_info[2]
            # print('stg_info', stg_info)
            stg_table_data_list.append(
                {'nav_date_week': stg_info[0], 'wind_code_str': stg_info[1], 'sample_name': sample_name})
        stg_table_df = pd.DataFrame(stg_table_data_list)

    print(stg_table_df)
