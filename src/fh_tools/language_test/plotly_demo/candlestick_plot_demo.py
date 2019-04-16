#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 19-4-11 上午9:21
@File    : candlestick_plot_demo.py
@contact : mmmaaaggg@163.com
@desc    : 
"""
import io
import pandas as pd
import plotly
import plotly.plotly as py
from plotly import figure_factory as FF
from datetime import datetime

plotly.tools.set_credentials_file(username='mmmaaaggg', api_key='YuQDcUpIZFGTJco0RRlp')

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

fig = FF.create_candlestick(df.Open, df.High, df.Low, df.Close, dates=df.Date)
py.iplot(fig, filename='candlestick', validate=False)

