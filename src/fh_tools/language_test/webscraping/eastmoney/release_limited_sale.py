# -*- coding: utf-8 -*-
"""
Created on 2018/2/7
@author: MG
"""
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from datetime import date, datetime, timedelta
import requests
import pandas as pd
from selenium import webdriver

browser = webdriver.Chrome(executable_path=r'd:\Downloads\fetch_eastmoney\chromedriver.exe')


def fetch_release_limited_sale(stock_code, output_path):
    """
    从东方财富网站抓取股票解禁数据，参考网址：http://data.eastmoney.com/dxf/q/300182.html
    :param stock_code: 股票代码
    :param output_path: 输出文件路径
    :return: 
    """
    url_str = "http://data.eastmoney.com/dxf/q/%s.html" % stock_code
    browser.get(url_str)
    browser.implicitly_wait(3)
    element_list = browser.find_elements_by_id('td_1')
    table = element_list[0]
    html = table.get_attribute('outerHTML')
    table_df_list = pd.read_html(html)
    if len(table_df_list) > 0:
        table_df = table_df_list[0]
        table_df.to_csv(output_path, index=False)


if __name__ == "__main__":
    stock_code = '300182'
    file_path = 'output.csv'
    fetch_release_limited_sale(stock_code, file_path)
    browser.close()
