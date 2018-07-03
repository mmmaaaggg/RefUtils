# -*- coding:utf-8 -*-
'''
Created on 2016年12月23日

@author: Family
'''
import pandas as pd
from datetime import datetime as dtime
#import matplotlib
#matplotlib.use('Agg')  # Agg 属性可以让图片不显示，直接保存成为图片
import matplotlib.pyplot as plt
from WindPy import *
from datetime import timedelta
import os

def windcode(code):
    return code + '.SH' if code[0] == '6' else code + '.SZ'

def date2datetime(dt):
    return dtime(dt.year, dt.month, dt.day)

def func(df, dfidx, pricefit, code, codeidx):
    df['return'+code] = df['CLOSE'] / pricefit - 1
    dfnew = df.join(dfidx, how='left', lsuffix=code, rsuffix=codeidx)
    dfnew['return'+codeidx] = dfnew['CLOSE'+codeidx] / dfnew['CLOSE'+codeidx][0] - 1
    return dfnew

ayearl = timedelta(days=350)
ayearh = timedelta(days=400)


datafilepath = '../Data/zengfashishi.xlsx'

dfall = pd.read_excel(datafilepath, sheetname='dingzeng', skiprows=0, header=1)

# print(dfall.head())
datetimecolnames = ['发行日期', '定价基准日', '股东大会公告日', '发审委审核公告日', '证监会审核公告日', '上市公告日', '限售解禁日']
for colname in datetimecolnames:
    dfall[colname] = pd.to_datetime(dfall[colname], format='%Y-%m-%d')
dfdatelen = dfall['限售解禁日']-dfall['发行日期']
dffilter = (ayearl < dfdatelen) & (dfdatelen < ayearh) & (dfall['限售解禁日']<dtime.strptime('2016-12-1', '%Y-%m-%d'))
# print(dfall[u'限售解禁日']<dtime.strptime('2016-12-1', '%Y-%m-%d'))
df = dfall[dffilter]
print((len(df)))
dfset = {}
w.start() # 启动 Wind API
codeidx = "000905.SH"
beginTime, endTime='2005-5-1', '2016-12-2'
key = codeidx + ' ' + beginTime + ' '+ endTime
fields = "close,pct_chg"
func = None
dfidx = WSDCache(w, key, func, codeidx, fields, beginTime, endTime, "PriceAdj=F")
statdic = {}
for idx in range(len(df)):  # len(df)
    datar = df.iloc[idx]
    code = str(datar['代码'])
    datefrm = datar['发行日期']
    dateto = datar['限售解禁日']
    pricezf = float(datar['发行价格'])
    pricet0 = float(datar['增发日收盘价'])
    
    key = dtime.strftime(datefrm, '%y-%m-%d ') + code
    dfnew = WSDCache(w, key, lambda x:func(x, dfidx, pricefit, code, codeidx), code, fields, datefrm, dateto, "PriceAdj=F")
    
    # filename = dtime.strftime(datefrm, '%y-%m-%d ') + code
    # 
    # filepath = r'../WindCache/' + filename + '.xls'
    # if os.path.exists(filepath):
    #     #print(u'%4d)read %s %s~%s'%(idx, code, datefrm, dateto))
    #     dfnew = pd.read_excel(filepath)
    # else:
    #     print(u'%4d)get %s %s~%s'%(idx, code, datefrm, dateto))
    #     wsd_data = w.wsd(code, "close,pct_chg", datefrm, dateto, "PriceAdj=F")
    #     close_first = wsd_data.Data[0][0]
    #     pricefit = pricezf * close_first / pricet0
    #     dfclose = pd.DataFrame(wsd_data.Data,index=wsd_data.Fields,columns=[date2datetime(d.date()) for d in wsd_data.Times]).T
    #     dfclose['return'+code] = dfclose['CLOSE'] / pricefit - 1
    #     dfnew = dfclose.join(dfidx, how='left', lsuffix=code, rsuffix=codeidx)
    #     dfnew['return'+codeidx] = dfnew['CLOSE'+codeidx] / dfnew['CLOSE'+codeidx][0] - 1
    #     dfnew.to_excel(filepath)
    colname_stat = 'stat_'+code
    statdic[colname_stat]=dfnew['return'+code]>0
    #dfclose['pct_chg_idx'] = 
    close_first = dfnew['CLOSE'+code][0]
    pricefit = pricezf * close_first / pricet0
    dfset[idx]={'code':code,
              'datefrm':datefrm,
              'dateto':dateto,
              'df':dfnew,
              'pricefit':pricefit,
              }
    # dfnew[['return'+code, 'return'+codeidx]].plot()
    # plt.show()
    # plt.savefig(filename + '.jpg')
    # plt.close()
dfstatset_all = pd.DataFrame(statdic)
dfstatset_pf = dfstatset_all[dfstatset_all.columns[(dfstatset_all==False).any()]] # 仅包含破发股票

def checklastbool(x, boolvalue):
    ret = x.dropna() == boolvalue
    return False if len(ret) == 0 else ret.iloc[-1]
dfstatset_pf_back = dfstatset_pf[dfstatset_pf.columns[dfstatset_pf.apply(lambda x:checklastbool(x, True))]] # 仅包含破发股票 后恢复的股票

def staticdf(df):
    # dfstatset_all[dfstatset_all==True] = 1
    # dfstatset_all[dfstatset_all==False] = -1
    # dfstatset_all.fillna(0)
    count1=(df==True).sum(axis=1)
    count2=(df==False).sum(axis=1) * (-1)
    # dfcount = pd.DataFrame({'down':count2, 'up':count1,'tot':count1-count2})
    dfcount = pd.DataFrame({'down':count2, 'up':count1,'tot':count1-count2, 'up ratio':count1/(count1-count2)})
    return dfcount

dfcount = staticdf(dfstatset_all)
dfcount_pf = staticdf(dfstatset_pf)
dfcount_pf_back = staticdf(dfstatset_pf_back)

dfnew = dfcount.join(dfcount_pf, how='left', rsuffix='pf').join(dfcount_pf_back, how='left', rsuffix='pfback').join(dfidx, how='left')
dfnew['return'] = dfnew['CLOSE'] / dfnew['CLOSE'][0]
# print('dfnew', dfnew.head())
#dfnew[['tot', 'up', 'down', 'return']].plot(grid=True, subplots=True, sharex=True)
dfnew[['up', 'uppf', 'uppfback', 'down', 'downpf', 'downpfback']].plot(grid=True)
plt.show()

# from WindPy import *
# from datetime import *
# w.start() # 启动 Wind API
# wsd_data = w.wsd("000905.SH", "close,pct_chg", "2006-05-01", "2016-12-23", "")
# dfindex=pd.DataFrame(wsd_data.Data,index=wsd_data.Fields,columns=wsd_data.Times).T
# dfindex.to_excel('../Data/000905SH.xlsx')
