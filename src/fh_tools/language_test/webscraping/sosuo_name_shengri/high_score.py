# -*- coding: utf-8 -*-
"""
Created on 2017/12/28
@author: MG
"""
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from datetime import date, datetime, timedelta


score_dic = {}
# http://www.sosuo.name/shengri/10-24-9-29
month, day = 9, 29
date_start = datetime.strptime("2016-01-01", "%Y-%m-%d").date()
for n, date_cur in enumerate([date_start + timedelta(days=nday) for nday in range(366)]):
    # print(n, date_cur)
    month, day = date_cur.month, date_cur.day
    url_str = r"http://www.sosuo.name/shengri/10-24-%d-%d" % (month, day)
    with urlopen(url_str) as rsp:
        html_str = rsp.read().decode('gb2312')
    bsobj = bs(html_str, "lxml")
    parent_result_list = bsobj.find_all("div", {"class": "h2_content"})

    for parent_result in parent_result_list:
        scroe_list = parent_result.find_all("strong")
        if scroe_list is None or len(scroe_list) == 0:
            continue
        # print(len(scroe_list))
        # print(scroe_list[1])
        try:
            score = int(scroe_list[1].contents[0])
        except:
            continue
        if score is not None:
            print(n, date_cur, score)
            score_dic[(month, day)] = score

print(score_dic)
