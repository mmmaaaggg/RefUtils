# -*- coding: utf-8 -*-
"""
Created on 2017/12/30
@author: MG
"""
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from datetime import date, datetime, timedelta
from requests import post

url_str = r"http://www.sse.com.cn/disclosure/listedinfo/periodic/"
url_str = r"http://query.sse.com.cn/infodisplay/queryBltnBookInfo.do?jsonCallBack=jsonpCallback46235&isPagination=true&isNew=1&bulletintype=L011&publishYear=2017&cmpCode=&startTime=&sortName=companyCode&direction=asc&" \
          r"pageHelp.pageSize=25&pageHelp.pageCount=50&pageHelp.pageNo=2&pageHelp.beginPage=2&pageHelp.cacheSize=1&pageHelp.endPage=21&_=1514614178902"
# with urlopen(url_str) as rsp:
#     html_str = rsp.read().decode('utf-8')
# bsobj = bs(html_str, "lxml")
# table_obj = bsobj.find_all("table", {"class": "table search_"})

url_str = r"http://query.sse.com.cn/infodisplay/queryBltnBookInfo.do"
param = {
    "jsonCallBack": "jsonpCallback63700",
    "isPagination": "true",
    "isNew": "1",
    "bulletintype": "L011",
    "publishYear": "2017",
    "cmpCode": "",
    "startTime": "",
    "sortName": "companyCode",
    "direction": "asc",
    "pageHelp.pageSize": "25",
    "pageHelp.pageCount": "50",
    "pageHelp.pageNo": "1",
    "pageHelp.beginPage": "1",
    "pageHelp.cacheSize": "1",
    "pageHelp.endPage": "5",
    # "_": "1514614178902",
}
resp = post(url_str)
html_str = resp.content

