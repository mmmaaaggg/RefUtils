# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 13:49:24 2017

@author: MGLaptop
"""

# -*- coding: utf-8 -*-
from datetime import datetime as dtime, timedelta

import numpy as np
import pandas as pd
from gmsdk.api import StrategyBase
from sklearn import svm

from src.fh_tools.fh_utils import utc2local

DateStrFormat = '%Y-%m-%d'
class MGStrategyBase(StrategyBase):
    # 对策略方法进行封装
    
    def open_long(self, bar, price, volume, comments=None):
        # print('bar type', type(bar), 'price', price, 'volume', volume, 'comments', comments)
        StrategyBase.open_long(self, bar.exchange, bar.sec_id, price, volume)
        if comments is not None:
            print((bar.strendtime, '开多', volume, comments))

    def close_long(self, bar, price, volume, comments=None):
        StrategyBase.close_long(self, bar.exchange, bar.sec_id, price, volume)
        if comments is not None:
            print((bar.strendtime, '平多', volume, comments))

    def close_long_yesterday(self, bar, price, volume, comments=None):
        StrategyBase.close_long_yesterday(self, bar.exchange, bar.sec_id, price, volume)
        if comments is not None:
            print((bar.strendtime, '平多', volume, comments))

    def open_short(self, bar, price, volume, comments=None):
        StrategyBase.open_short(self, bar.exchange, bar.sec_id, price, volume)
        if comments is not None:
            print((bar.strendtime, '开空', volume, comments))

    def close_short(self, bar, price, volume, comments=None):
        StrategyBase.close_short(self, bar.exchange, bar.sec_id, price, volume)
        if comments is not None:
            print((bar.strendtime, '平空', volume, comments))

    def close_short_yesterday(self, bar, price, volume, comments=None):
        StrategyBase.close_short_yesterday(self, bar.exchange, bar.sec_id, price, volume)
        if comments is not None:
            print((bar.strendtime, '平空', volume, comments))

def perpare_data(rets, datalen):
    return rets[-datalen:]

def perpare_traindata(rets, datalen, dataX=None, dataY=None):
    retlen = len(rets)
    samplecount = retlen - datalen
    if dataX is None:
        dataX, dataY = [], []
    for n in range(len(dataX), samplecount):
        dataX.append(rets[n:n+datalen])
        dataY.append(1 if rets[n+datalen] > 0.01 else 0)
    return dataX, dataY

def checkpredict(predict, ret):
    datay = 1 if ret > 0.01 else 0
    return datay == predict

def train(dataX, dataY):
    clf = svm.SVC()  # class   
    clf.fit(dataX, dataY)  # training the svc model
    return clf  
        
class Mystrategy(MGStrategyBase):
    def __init__(self, *args, **kwargs):
        super(Mystrategy, self).__init__(*args, **kwargs)
        self.logs = []

        # 六个关键价格
        self.buy_setup = 0
        self.sell_setup = 0
        self.buy_break = 0
        self.sell_break = 0
        self.buy_enter = 0
        self.sell_enter = 0
        
        # 是否当日是否触及 观察买入、观察卖出价
        self.hasUnderBuySetup = False
        self.hasAboveSellSetup = False
        self.targetCount = 10
        self.datetime_curcloseday = None
        # 日内最晚买入时间是否有效
        self.datetime_stopopen_available = False
        # 日内平仓时间是否有效
        self.datetime_closeposition_available = False
        self.histdf = None
        self.date_latesthis = None
        self.lastpredict = None
        self.predictresults = []
        self.clf = None
        self.dataX = None
        self.dataY = None

    def calckeyprices(self): # , bar
        # ndays= 20
        tradedate_curr = dtime.today() - timedelta(days=1)
        date_lastday = (tradedate_curr - timedelta(days=1)).strftime(DateStrFormat)
        if self.date_latesthis is None:
            self.date_latesthis = dtime.strptime('2005-01-01', DateStrFormat).date()
        else:
            #　date_lastnday = (tradedate_curr - timedelta(days=ndays)).strftime('%Y-%m-%d')
            self.date_latesthis = self.date_latesthis + timedelta(days=1)
        date_lastnday = dtime.strftime(self.date_latesthis, DateStrFormat)
        # '.'.join([bar.exchange, bar.sec_id])
        dbarslastndays = self.get_dailybars('SHFE.rb', date_lastnday, date_lastday)
        dates, opens, highs, lows, closes, vols, pre_closes = [], [], [], [], [], [], []
        for dbar in dbarslastndays:
            dates.append(utc2local(dbar.utc_time))
            opens.append(dbar.open)
            highs.append(dbar.high) 
            lows.append(dbar.low)
            closes.append(dbar.close) 
            vols.append(dbar.volume)
            pre_closes.append(dbar.pre_close)
        hisdic = {'open':opens,
                  'high':highs,
                  'low':lows,
                  'close':closes,
                  'vol':vols,
                  'pre_close':pre_closes,
                  }
        # print('hisdic', len(hisdic), 'data len', len(opens))
        histdf = pd.DataFrame(hisdic, index=dates)
        rets = histdf['close'] / histdf['pre_close'] - 1
        rets[np.isinf(rets)] = 0
        histdf['return'] = rets
        if self.histdf is None:
            self.histdf = histdf
            print((self.histdf.head()))
        else:
            self.histdf = pd.concat([self.histdf, histdf])
        
        retdata = self.histdf['return']
        if self.lastpredict is not None:
            result = checkpredict(self.lastpredict, retdata[-1])
            self.predictresults.append(result)
        unavailabledata = np.isnan(retdata) | np.isinf(retdata)
        if sum(unavailabledata) > 0:
            print(('nan or inf data:', retdata.index[unavailabledata]))
            retdata[unavailabledata] = 0
        datalen = 20
        if self.histdf.shape[0] % 50 == 0:
            print((self.histdf[['close', 'return']].tail()))
            print('perpare data and train')
            time1 = dtime.now()
            self.dataX, self.dataY = perpare_traindata(retdata, datalen, self.dataX, self.dataY)
            time2 = dtime.now()
            self.clf = train(self.dataX, self.dataY)
            time3 = dtime.now()
            print(('time estimates:\nperpare_traindata:',time2-time1,
                  'train:', time3-time2))
            predictresultcount = len(self.predictresults)
            if predictresultcount > 0:
                predictresult_truecount = sum(self.predictresults)
                print(('svm predict [%d/%d] = %.0f%%'%(predictresult_truecount, predictresultcount,
                                                      float(predictresult_truecount)/predictresultcount*100)))
        if self.clf is not None:
            dataX = perpare_data(retdata, datalen)
            self.lastpredict = self.clf.predict(np.array(dataX).reshape((1,-1)))
        
myStrategy = Mystrategy(
    username='13522870868',
    password='123456',
    strategy_id='25bebdc5-d958-11e6-a497-0023aee71d20',
    subscribe_symbols='SHFE.RB.bar.60',
    mode=4,
    td_addr='localhost:8001'
)
timeStart = dtime.now()
myStrategy.backtest_config(
    start_time='2016-1-01 09:00:00',
    end_time='2016-12-30 15:00:00',
    initial_cash=1000000,
    transaction_ratio=1,
    commission_ratio=0.00004,
    slippage_ratio=0.0001,
    price_type=0)
myStrategy.calckeyprices()
timeEnd = dtime.now()
timeEstimate = timeEnd - timeStart
print((f1, f3, 'finished at', timeEnd, 'Estimation:', timeEstimate))


