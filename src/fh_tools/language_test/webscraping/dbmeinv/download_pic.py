# -*- coding: utf-8 -*-
"""
Created on 2017/8/13
@author: MG
"""

from urllib.request import urlopen
import urllib.request
from bs4 import  BeautifulSoup
import os,sys,time
import http.cookiejar

path = os.getcwd()
new_path = os.path.join(path, u'豆瓣妹子')
if not os.path.isdir(new_path):
    os.mkdir(new_path)

def makeMyOpener(head={
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
}):
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    header = []
    for key, value in head.items():
        elem = (key, value)
        header.append(elem)
    opener.addheaders = header
    return opener
def crawl_loop(index):
    oper = makeMyOpener()
    url = 'http://www.dbmeinv.com/dbgroup/show.htm?pager_offset=%s' % index
    html = oper.open(url)
    bsObj = BeautifulSoup(html)
    girl_list = bsObj.findAll('img')
    if not girl_list:
        print(u'已经全部抓取完毕')
        sys.exit(0)

    print(u'开始抓取')
    print("====================================================================================")
    for girl in girl_list:
        link = girl.get('src')
        try:
            content = urlopen(link).read()
            with open(u'豆瓣妹子'+'/'+link[-11:], 'wb') as code:
                code.write(content)
        except TimeoutError as e:
            print(e)

    index = int(index)+1
    print(u'开始抓取下一页')
    print('第 %s 页' % index)
    time.sleep(1)
    crawl_loop(index)
crawl_loop(119)
