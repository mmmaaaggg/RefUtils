#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/11/6 15:07
@File    : grid_test.py
@contact : mmmaaaggg@163.com
@desc    : 
"""

from pyecharts.charts import Line, Pie, Grid

# configure(output_image=True)

line = Line("折线图示例", width=1200)
attr = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
line.add("最高气温", attr, [11, 11, 15, 13, 12, 13, 10],
         mark_point=["max", "min"], mark_line=["average"])
line.add("最低气温", attr, [1, -2, 2, 5, 3, 2, 0], mark_point=["max", "min"],
         mark_line=["average"], legend_pos="20%")
attr = ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]
v1 = [11, 12, 13, 10, 10, 10]
pie = Pie("饼图示例", title_pos="45%")
pie.add("", attr, v1, radius=[30, 55],
        legend_pos="65%", legend_orient='vertical')

grid = Grid()
grid.add(line, grid_right="65%")
grid.add(pie, grid_left="60%")
grid.render(path='grid.pdf', delay=3)
