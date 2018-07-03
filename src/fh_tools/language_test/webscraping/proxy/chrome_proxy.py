#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/3/8 19:33
@File    : chrome_proxy.py
@contact : mmmaaaggg@163.com
@desc    : 
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from datetime import date, datetime, timedelta
import requests
import pandas as pd
from selenium import webdriver
import random


def get_proxy_list():
    """
    自动获取代理地址列表
    :return:
    """
    url_str = 'http://31f.cn/'
    proxy_df = pd.read_html(url_str,header=1)[0]
    proxy_list = list(proxy_df.apply(lambda x: '%s:%s' % (x[1], x[2]), axis=1))
    return proxy_list


def getHtml(browser, url):
    proxy_support = request.ProxyHandler({"http": proxy_address})
    opener = request.build_opener(proxy_support)
    request.install_opener(opener)
    with request.urlopen(url) as rsp:
        html_str = rsp.read()
    return html_str


proxies = get_proxy_list()
random_proxy = random.choice(proxies)
url_str = "https://www.baidu.com/s?wd=%E7%8A%80%E7%89%9B%E8%81%94%E7%9B%9F"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=http://%s' % random_proxy)
browser = webdriver.Chrome(executable_path=r'd:\Softwares\Chrome\chromedriver.exe')  # , chrome_options=chrome_options
browser.get(url_str)
browser.implicitly_wait(3)
element_list = browser.find_elements_by_id('td_1')