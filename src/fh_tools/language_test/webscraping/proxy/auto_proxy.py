#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/3/8 17:14
@File    : auto_proxy.py
@contact : mmmaaaggg@163.com
@desc    : 自动寻找代理列表，每一次访问随机切换不同代理，连续方位某一个网址
"""

import urllib.request as request
import pandas as pd
import random
import sys


def get_proxy_list():
    """
    自动获取代理地址列表
    :return:
    """
    url_str = 'http://31f.cn/'
    proxy_df = pd.read_html(url_str,header=1)[0]
    proxy_list = list(proxy_df.apply(lambda x: '%s:%s' % (x[1], x[2]), axis=1))
    return proxy_list


def getHtml(url, proxy_address):
    """
    访问某一个网址
    :param url:
    :param proxy_address:
    :return:
    """
    proxy_support = request.ProxyHandler({"http": proxy_address})
    opener = request.build_opener(proxy_support)
    request.install_opener(opener)
    with request.urlopen(url) as rsp:
        html_str = rsp.read()
    return html_str


# def get_page_n_url(html_str):
#     bsobj = bs(html_str, "lxml")


# url = "https://www.baidu.com/s?wd=%E7%8A%80%E7%89%9B%E8%81%94%E7%9B%9F"

def auto_proxy_goto(url_str, times=1000):
    """
    自动切换代理，访问该网页 times 次
    :param url_str:
    :param times:
    :return:
    """
    # proxies = ["111.155.116.225:8123", "203.174.112.13:3128", '122.114.31.177:808']
    proxies = get_proxy_list()
    for i in range(times):
        try:
            random_proxy = random.choice(proxies)
            html = getHtml(url_str, random_proxy)

            print(i, ')', random_proxy, '*' * 20, 'ok')  # 打印网页的头部信息，只是为了展示访问到了网页，可以自己修改成想显示的内容
        except Exception as exp:
            print(i, '*' * 20, random_proxy, "出现故障", exp)


if __name__ == "__main__":
    url_str = 'https://www.baidu.com/link?url=jSMKzoXLmo3g80bNR1GtDpipiUyE6gIRTLIcwp-kR0GmEjdXTJnd-MyGwgLNZ_Jj&wd=&eqid=87e00dd70005c558000000035aa12814'
    url_str = sys.argv[1]
    times = int(sys.argv[2])
    print('访问%d次网址:' % times, url_str)
    auto_proxy_goto(url_str, times)
