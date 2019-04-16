#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 19-4-11 上午9:11
@File    : candle_demo2.py.py
@contact : mmmaaaggg@163.com
@desc    : 
"""

#The following example, downloads stock data from Yahoo and plots it.
from pandas.io.data import get_data_yahoo
import matplotlib.pyplot as plt

from matplotlib.pyplot import subplots, draw
from matplotlib.finance import candlestick

symbol = "GOOG"

data = get_data_yahoo(symbol, start = '2013-9-01', end = '2013-10-23')[['Open','Close','High','Low','Volume']]

ax = subplots()

candlestick(ax,data['Open'],data['High'],data['Low'],data['Close'])

if __name__ == "__main__":
    pass
