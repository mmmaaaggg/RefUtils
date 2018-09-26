#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/9/12 16:08
@File    : quan_shang_li_cai_gui_mo_tong_ji.py
@contact : mmmaaaggg@163.com
@desc    : 
"""
import pandas as pd
from src.fh_tools.fh_utils import is_nan_or_none, is_not_nan_or_none

file_path = r"d:\Downloads\短期纯债券商集合理财计划产品规模.xlsx"
data_df = pd.read_excel(file_path)
available_df = data_df[data_df['基金规模'].apply(is_not_nan_or_none)]
q = [1, 0.8, 0.6, 0.5, 0.4, 0.2, 0]
quantile_df = available_df.quantile(q)
print('基金规模分位数统计:\n%s' % quantile_df)
