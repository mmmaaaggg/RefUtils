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
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as bs

# browser = webdriver.Chrome(executable_path=r'd:\Softwares\Chrome\chromedriver.exe')


def fetch_release_limited_sale(page_num, output_path):
    """
    从东方财富网站抓取股票解禁数据，参考网址：http://data.eastmoney.com/dxf/q/300182.html
    :param page_num: 股票代码
    :param output_path: 输出文件路径
    :return: 
    """
    url_str = "http://q.stock.sohu.com/jlp/analyst/info.up?analystCode=303044917&pageNum=%d#page" % page_num
    with urlopen(url_str) as rsp:
        html_str = rsp.read().decode('gbk')
        bsobj = bs(html_str)
    # print(bsobj)
    obj_list = bsobj.find_all(class_="table yjytable")
    table = obj_list[0]
    # html = table.get_attribute('outerHTML')
    table_df_list = pd.read_html(str(table))
    if len(table_df_list) > 0:
        table_df = table_df_list[0]
        table_df.to_csv(output_path, index=False, encoding='utf-8')


if __name__ == "__main__":
    page_num = 2
    file_path = 'output.csv'
    fetch_release_limited_sale(page_num, file_path)
    # browser.close()
