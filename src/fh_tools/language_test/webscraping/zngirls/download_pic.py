# -*- coding: utf-8 -*-
"""
Created on 2017/8/13
@author: MG
"""

# coding:utf-8
from urllib.error import URLError
from urllib.parse import urlencode, unquote
from urllib.request import Request, urlopen
import re, os
from urllib import *
from time import sleep


class spider:
    def __init__(self):
        self.lst_girl = []
        self.lst_fail = []
        self.lst_use = []
        self.PATH = os.getcwd()
        self.host = 'http://www.zngirls.com'

    def saveimg(self, fdir, img_url):
        fn = img_url.split('/')
        try:
            data = urllib2.urlopen(img_url, timeout=20).read()
            f = open(fdir + '\\' + fn[-1], 'wb')
            f.write(data)
            f.close()
            print('save image ===========  ok')
        except:
            print('save image error ==== OK')
            f = open(fdir + '\\err.txt', 'w')
            f.write(img_url)
            f.close()

    def mkdir(self, fdir):
        ie = os.path.exists(fdir)
        if not ie:
            os.makedirs(fdir)

    # 获取所有列表
    def getgirllist(self):
        url = 'http://www.zngirls.com/ajax/girl_query_total.ashx'
        c = '%E9%9F%A9%E5%9B%BD'  # country棒子
        # p='%E8%BD%A6%E6%A8%A1'  #模特
        tmp = unquote(c)
        # temp=unquote(p)     #url double encode
        country = unquote(tmp)
        # profe=unquote(temp)
        hd = {'Host': 'www.zngirls.com',
              'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:17.0) Gecko/20100101 Firefox/17.0',
              'Referer': 'http://www.zngirls.com/find/',
              'X-Requested-With': 'XMLHttpRequest'
              }
        i = 1
        go = True
        lst_count = []
        while go:
            postdata = {'country': country,
                        'curpage': str(i),
                        'pagesize': '20'
                        }
            post_data = urlencode(postdata)
            req = Request(url, post_data, hd)
            html = urlopen(req).read()
            pat = re.compile('/girl/[\d]+')
            lst_url = re.findall(pat, html)
            lst_count += lst_url
            print('初始化完成页数: ' + str(i))
            if len(lst_url) > 1:
                go = True
                i += 1
            else:
                go = False

        glst = list(set(lst_count))
        file_name = 'list.txt'
        file_path= self.get_file_path(file_name)
        fp = open(file_path, 'w')
        for s in glst:
            fp.write(s + '\n')
        fp.close()
        print('初始化完成 ================ OK')
        print('获取数据长度: ' + str(len(glst)))
        return glst

    def get_file_path(self, file_name):
        base_dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(base_dir_path, file_name)
        return file_path

    # 处理数据
    def solvedata(self, html):
        pat = re.compile("value='(.*?)'")
        found = re.findall(pat, html)

        ipat = re.compile('<td colspan="3">(.*?)</textarea></td>', re.S)
        tmp = ipat.search(html).group(1)
        info = re.sub('<[^>]+>', '', tmp)
        info = info.replace('&nbsp;', '')
        fdir = os.getcwd() + '\\spider\\' + found[0]
        print(fdir)
        self.mkdir(fdir)
        fp = open(fdir + '\\list.txt', 'w')
        for opt in found:
            fp.write(opt + '\n')
        fp.write(info)
        fp.close()
        print('write file ======  ok')
        # ===image ================
        im = re.compile("class='imglink' href='(.*?)'><img", re.I)
        imglink = im.search(html).group(1)
        self.saveimg(fdir, imglink)

    def main(self):
        url = 'http://www.zngirls.com'
        file_name = 'list.txt'
        file_path= self.get_file_path(file_name)
        fp = open(file_path, 'r')
        buf = fp.read()
        if len(buf) < 250:
            self.lst_girl = self.getgirllist()
        else:
            self.lst_girl = buf.split('\n')
            print('读取缓冲完成 === ok')
        print('数据长度:  ' + str(len(self.lst_girl)))

        hd = {'Host': 'www.zngirls.com',
              'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:17.0)',
              'Referer': 'http://www.zngirls.com/'
              }
        for s in self.lst_girl:
            g_url = url + s
            if os.path.exists(os.getcwd() + '\\spider\\' + s[s.rfind('/') + 1:]):
                print(s + 'exist')
            else:
                try:
                    req = urllib2.Request(g_url, headers=hd)
                    html = urllib2.urlopen(req).read()
                    self.solvedata(html)
                    # self.lst_use.append(s)
                    sleep(2)
                except URLError as e:
                    self.lst_fail.append(s)
                    print('1.error:' + str(e.reason))
                    sleep(5)
        fp = open('err.txt', 'w')
        for err in self.lst_fail:
            fp.write(err + '\n')
        fp.close()
        print("spider success")


craw = spider()
craw.main()
