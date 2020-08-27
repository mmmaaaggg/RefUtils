"""
@author  : MG
@Time    : 2020/8/27 11:32
@File    : guo3.py
@contact : mmmaaaggg@163.com
@desc    : 翻译 Guo3.R Guo4.R文件
"""
import sqlite3
import os
import pandas as pd
import numpy as np

file_path = r'C:\Users\26559\Downloads\Guo\FuJuCode2.csv'
code_s = pd.read_csv(file_path)["Code"]

sector_class_dic = {}
db_file_path = r"C:\Users\26559\Downloads\Guo\DB_SectorClassification.db"
date_s = None  # gou4.py 里面要用到
date_count = 0
with sqlite3.connect(db_file_path) as conn:
    # table_name_s = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name", conn)["name"]
    for num, code in enumerate(code_s, start=1):
        table_name = f"X{code[:6]}"
        print(f"{num:4d}) {code} -> {table_name}")
        stock_df = pd.read_sql(f"select * from {table_name}", conn)
        if date_s is None:
            date_s = pd.to_datetime(stock_df['Date'])
            date_count = stock_df.shape[0]
        sector_class_dic[code] = stock_df["TYPE_ID"]
        # if num > 3:  # 调试使用
        #     break

sector_class_df = pd.DataFrame(sector_class_dic)
sector_class_df.fillna(0)
#          000001.SZ     000002.SZ     000004.SZ     000005.SZ
# 0     1.031721e+10  1.031723e+10  1.031718e+10  1.031723e+10
# 1     1.031721e+10  1.031723e+10  1.031718e+10  1.031723e+10
# 2     1.031721e+10  1.031723e+10  1.031718e+10  1.031723e+10
# 3     1.031721e+10  1.031723e+10  1.031718e+10  1.031723e+10
# 4     1.031721e+10  1.031723e+10  1.031718e+10  1.031723e+10
#             ...           ...           ...           ...
# 3309  1.031721e+10  1.031723e+10  1.031718e+10  1.031704e+10
# 3310  1.031721e+10  1.031723e+10  1.031718e+10  1.031704e+10
# 3311  1.031721e+10  1.031723e+10  1.031718e+10  1.031704e+10
# 3312  1.031721e+10  1.031723e+10  1.031718e+10  1.031704e+10
# 3313  1.031721e+10  1.031723e+10  1.031718e+10  1.031704e+10
# 取前8位
sector_class2_df = sector_class_df.applymap(lambda x: str(int(x))[:8])
sector_unique_list = [_ for _ in set(sector_class2_df.to_numpy().flatten()) if _ != '0']
sector_unique_list.sort()
sector_count = len(sector_unique_list)

# Guo4.R
folder_path = r'C:\Users\26559\Downloads\Guo\DataConsDataYes\ZZ500'
year_s = date_s.apply(lambda x: x.year)
month_s = date_s.apply(lambda x: x.month)
file_list = os.listdir(folder_path)
file_list.sort()
file_count = len(file_list)
cons_dic = {}
from_n = 23
for num, file_name in enumerate(file_list[from_n:], start=from_n + 1):
    print(f"{num:2d}) {file_name}")
    df = pd.read_csv(os.path.join(folder_path, file_name), index_col=0, encoding='GBK')
    del df['Date']
    # 感觉逻辑有点问题会不会用了未来数据了？
    if num < file_count:
        # 下一个文件
        file_name_year = int(file_list[num][4:8])
        file_name_month = int(file_list[num][9:11])
        indexes = np.where((year_s == file_name_year) | (month_s == file_name_month))[0]
    else:
        # 当前文件
        file_name_year = int(file_name[4:8])
        file_name_month = int(file_name[9:11])
        indexes = np.where((year_s == file_name_year) | (month_s == file_name_month))[0]
        indexes = range(indexes[-1] + 1, date_count + 1)

    for _ in indexes:
        cons_dic[_] = df

    # break

for key in cons_dic.keys():
    cons = cons_dic[key]
    # break
    # 对板块权重进行归一化操作
    weight_s = cons['Weight']
    weight_na_s = weight_s.isna()
    na_count = sum(weight_na_s)
    if na_count > 0:
        weight_s[weight_na_s] = (100 - weight_s.dropna().sum()) / na_count

# 取行业的权重 #
index_sector = np.zeros((date_count, sector_count))
for t in range(date_count):
    for i in range(sector_count):
        cons = cons_dic[t]
        sector = sector_unique_list[i]
        sector_s = sector_class2_df.iloc[t, :]
        stock_codes = sector_s[sector_s == sector].index
        index_sector[t, i] = cons[np.isin(cons.index, stock_codes)]['Weight'].sum()

# normalize
index_sector_x = np.zeros_like(index_sector)
for _ in range(index_sector.shape[1]):
    index_sector_x[:, _] = index_sector[:, _] / index_sector.sum(axis=1)

file_path = r'C:\Users\26559\Downloads\Guo\IndexZZ500.csv'
index_df = pd.read_csv(file_path)
index_open_s = index_df['Open']
index_high_s = index_df['High']
index_low_s = index_df['Low']
index_close_s = index_df['Close']
index_re = index_close_s.pct_change()[1:] / index_close_s[:-1]
