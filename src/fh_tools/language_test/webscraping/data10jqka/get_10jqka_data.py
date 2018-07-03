# -*- coding: utf-8 -*-
"""
Created on 2017/8/23
@author: MG
"""

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as bs

url_str = r"http://data.10jqka.com.cn/market/rzrqgg/code/601318/"
with urlopen(url_str) as rsp:
    html_str = rsp.read().decode('gbk')
    bsobj = bs(html_str)
# print(bsobj)
obj_list = bsobj.find_all(class_="tr c-rise")
result_list = []
for obj in obj_list:
    tr_obj = obj.parent
    date_str = tr_obj.find(class_="tc cur").content
    amount_str = obj.contents
    result_list.append({"date_str": date_str, "amount_str": amount_str})
print(result_list)