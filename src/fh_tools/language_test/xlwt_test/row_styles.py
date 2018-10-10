#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2005 Kiseliov Roman
# https://github.com/python-excel/xlwt/blob/master/examples/row_styles.py

from xlwt import *

w = Workbook()
ws = w.add_sheet('Hey, Dude')

for i in range(6, 80):
    fnt = Font()
    fnt.height = i*20
    style = XFStyle()
    style.font = fnt
    ws.write(i, 1, 'Test')
    ws.row(i).set_style(style)
w.save('row_styles.xls')
