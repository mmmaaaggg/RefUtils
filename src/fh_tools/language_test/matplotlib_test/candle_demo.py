#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 19-4-11 上午9:05
@File    : candle_demo.py
@contact : mmmaaaggg@163.com
@desc    : 
"""
import io
from math import pi
import pandas as pd
from bokeh.plotting import figure, show, output_file


def show_plot():

    df = pd.read_csv(
        io.BytesIO(
            b'''Date,Open,High,Low,Close
    2016-06-01,69.6,70.2,69.44,69.76
    2016-06-02,70.0,70.15,69.45,69.54
    2016-06-03,69.51,70.48,68.62,68.91
    2016-06-04,69.51,70.48,68.62,68.91
    2016-06-05,69.51,70.48,68.62,68.91
    2016-06-06,70.49,71.44,69.84,70.11
    2016-06-07,70.11,70.11,68.0,68.35'''
        )
    )

    df["Date"] = pd.to_datetime(df["Date"])

    inc = df.Close > df.Open
    dec = df.Open > df.Close
    w = 12 * 60 * 60 * 1000

    TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

    p = figure(x_axis_type="datetime", tools=TOOLS, plot_width=1000, title
    ="Candlestick")
    p.xaxis.major_label_orientation = pi / 4
    p.grid.grid_line_alpha = 0.3

    p.segment(df.Date, df.High, df.Date, df.Low, color="black")
    p.vbar(df.Date[inc], w, df.Open[inc], df.Close[inc], fill_color="#D5E1DD", line_color="black")
    p.vbar(df.Date[dec], w, df.Open[dec], df.Close[dec], fill_color="#F2583E", line_color="black")

    output_file("candlestick.html", title="candlestick.py example")

    show(p)


if __name__ == "__main__":
    show_plot()
