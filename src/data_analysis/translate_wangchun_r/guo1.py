"""
@author  : MG
@Time    : 2020/8/27 11:04
@File    : guo1.py
@contact : mmmaaaggg@163.com
@desc    : 翻译 Guo1.R文件pct_change
"""
import pandas as pd
import numpy as np

file_path = r'C:\Users\26559\Downloads\Guo\equal_weighted.csv'
df = pd.read_csv(file_path, index_col=[0])
fv = df.fillna(-100)

close_df = pd.DataFrame()  # close_df  数据在其他地方获取，类型为 DataFrame
cc = (df.pct_change().iloc[1:, :] / df.iloc[:-1, :]).fillna(0)
log_close_df = np.log(close_df)
log_cc = log_close_df.pct_change().iloc[1:, :].fillna(0)
