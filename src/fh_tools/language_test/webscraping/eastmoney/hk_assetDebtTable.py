#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/9/12 11:21
@File    : hk_assetDebtTable.py
@contact : mmmaaaggg@163.com
@desc    : pip install selenium
"""
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from datetime import date, datetime, timedelta
import requests
import pandas as pd
from selenium import webdriver

browser = webdriver.Chrome(executable_path=r'd:\Softwares\Chrome\chromedriver.exe')


def fetch_asset_debt_table(stock_code, output_path):
    """
    从东方财富网站抓取港股资产负债表，参考网址：http://hkf10.eastmoney.com/html_HKStock/index.html?securitycode=02611&name=assetDebtTable
    :param stock_code: 股票代码
    :param output_path: 输出文件路径
    :return:
    """
    url_str = "http://hkf10.eastmoney.com/html_HKStock/index.html?securitycode=%s&name=assetDebtTable" % stock_code
    # url_str = "http://data.eastmoney.com/dxf/q/%s.html" % stock_code
    browser.get(url_str)
    browser.implicitly_wait(3)
    element_list = browser.find_elements_by_id('table_assetDebt_tableFixClone')
    table = element_list[0]
    html = table.get_attribute('outerHTML')
    table_df_list = pd.read_html(html)
    if len(table_df_list) > 0:
        table_df = table_df_list[0]
        table_df.to_csv(output_path, index=False, encoding='GBK')
        print(table_df)


if __name__ == "__main__":
    stock_code = '02611'
    file_path = 'output.csv'
    fetch_asset_debt_table(stock_code, file_path)
    browser.close()
