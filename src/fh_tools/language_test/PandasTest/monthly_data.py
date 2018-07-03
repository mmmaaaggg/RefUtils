# -*- coding: utf-8 -*-
"""
Created on 2017/12/20
@author: MG
"""
import pandas as pd
from datetime import date, datetime, timedelta

data_df = pd.read_csv(r"D:\Downloads\TrendFollowingDifficultyDaily.csv")
data_df["DateObj"] = data_df["Date"].apply(lambda x: datetime.strptime(x, "%Y-%m-%d"))
data_df['ym'] = data_df["DateObj"].apply(lambda x: x.year * 100 + x.month // 3)  # 每三个月一次
data_dfg = data_df.groupby('ym')
monthly_df = data_dfg.apply(lambda x: x.iloc[-1])
monthly_df.to_csv('monthly.csv')
