#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 19-6-10 上午9:59
@File    : find_available_chinese_fonts.py
@contact : mmmaaaggg@163.com
@desc    : 寻找matplotlib和Ubuntu都能用的中文字体 (原文源代码)
"""

__author__ = 'Katherine'
from matplotlib.font_manager import FontManager
import subprocess


def get_chinese_font_iter():
    fm = FontManager()
    mat_fonts = set(f.name for f in fm.ttflist)

    output = subprocess.check_output(
        'fc-list :lang=zh -f "%{family}\n"', shell=True)
    output = output.decode('utf-8')
    # print '*' * 10, '系统可用的中文字体', '*' * 10
    # print output
    zh_fonts = set(f.split(',', 1)[0] for f in output.split('\n'))
    available = mat_fonts & zh_fonts
    yield from available

    # print('*' * 10, '可用的字体', '*' * 10)
    # for num, f in enumerate(available, start=1):
    #     print(num, ')', f)


def _test_get_chinese_font_iter():
    print('*' * 10, '可用的字体', '*' * 10)
    for num, f in enumerate(get_chinese_font_iter(), start=1):
        print(f'{num}) {f}')


if __name__ == "__main__":
    _test_get_chinese_font_iter()
