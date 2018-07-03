# -*- coding: utf-8 -*-
"""
Created on 2017/7/29
@author: MG
"""
import pandas as pd


file_path = r'd:\Downloads\Account600030.xls'
data_df = pd.read_excel(file_path)

import xlrd
# 获取一个Book对象
book = xlrd.open_workbook(file_path)

# 获取一个sheet对象的列表
sheets = book.sheets()
# 遍历每一个sheet，输出这个sheet的名字（如果是新建的一个xls表，可能是sheet1、sheet2、sheet3）
for sheet in sheets:
    print(sheet.name)
