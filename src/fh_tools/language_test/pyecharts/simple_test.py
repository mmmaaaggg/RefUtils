#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/11/6 14:46
@File    : simple_test.py
@contact : mmmaaaggg@163.com
@desc    : 
"""
from unittest import mock


def get_chrome_driver():
    from selenium import webdriver
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(options=options)


from snapshot_selenium import snapshot as driver

from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.render import make_snapshot


def bar_chart() -> Bar:
    c = (
        Bar()
        .add_xaxis(["衬衫", "毛衣", "领带", "裤子", "风衣", "高跟鞋", "袜子"])
        .add_yaxis("商家A", [114, 55, 27, 101, 125, 27, 105])
        .add_yaxis("商家B", [57, 134, 137, 129, 145, 60, 49])
        .reversal_axis()
        .set_series_opts(label_opts=opts.LabelOpts(position="right"))
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar-测试渲染图片"))
    )
    return c


with mock.patch('snapshot_selenium.snapshot.get_chrome_driver', get_chrome_driver):
    # 需要安装 snapshot-selenium 或者 snapshot-phantomjs
    make_snapshot(driver, bar_chart().render(), "bar.png")
