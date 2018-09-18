#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2005 Kiseliov Roman
# 参考 ：https://github.com/python-excel/xlwt/blob/master/examples/dates.py

from datetime import datetime

from xlwt import *

w = Workbook()
ws = w.add_sheet('Hey, Dude')

fmts = [
    'YYYY/M/D',
    'YY/MM/DD',
    'M/D/YY',
    'D-MMM-YY',
    'D-MMM',
    'MMM-YY',
    'h:mm AM/PM',
    'h:mm:ss AM/PM',
    'h:mm',
    'h:mm:ss',
    'M/D/YY h:mm',
    'mm:ss',
    '[h]:mm:ss',
    'mm:ss.0',
]

i = 0
for fmt in fmts:
    ws.write(i, 0, fmt)

    style = XFStyle()
    style.num_format_str = fmt

    ws.write(i, 4, datetime.now(), style)

    i += 1

w.save('dates.xls')