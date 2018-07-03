# -*- coding: utf-8 -*-
import tushare as ts


df = ts.get_realtime_quotes('000581') #Single stock symbol
# df[['code','name','price','bid','ask','volume','amount','time']]
print(df)
