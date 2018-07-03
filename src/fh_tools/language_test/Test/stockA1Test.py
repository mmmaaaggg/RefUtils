# -*- coding: utf-8 -*-
"""Created on Thu Feb 23 23:55:13 2017
@author: caoyu
"""

import sqlalchemy as sa
import pandas as pd

engine = sa.create_engine('mysql+pymysql://testfh:64776348@nas.orientever.com:33006/test?charset=utf8')
conn = engine.connect()
# engine.echo=True
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.ticker as ticker
# from matplotlib.finance import candlestick2_ohlc
from matplotlib.finance import candlestick_ohlc


def showMACDresult(startdate=None, enddate=None):
    array = []

    show_str = ""
    if enddate is None:
        enddate = pd.read_sql(u"SELECT MAX(tday) FROM sectorprice", engine).iat[0, 0]
    if startdate is None:
        startdate = enddate
    sql = u''' SELECT DISTINCT t.sec_name, t.wind_code, f.bull, f.bear, f.turn05, f.turn520,
f.TID, t.reason, t.classes FROM ticketfeature AS f INNER JOIN tickets AS t
ON f.TID = t.TID AND t.inpool = 1 INNER JOIN tsmap AS m ON t.TID = m.TID '''
    sqls = u''' SELECT p.tday, p.SID, p.alertMACD, s.wind_code, s.sec_name FROM sectorprice
AS p INNER JOIN sectors AS s ON p.SID = s.SID WHERE p.alertMACD <> 0 AND p.tday
BETWEEN "%s" AND "%s"; ''' % (startdate, enddate)
    df = pd.read_sql(sqls, engine)

    def _bullbear(x):
        if x['bull'] and x['bear']:
            return u'多+空'
        elif x['bull'] and not (x['bear']):
            return u'多头'
        elif not (x['bull']) and x['bear']:
            return u'空头'
        else:
            return u'无'

    def _keywords(x):
        if x > 0:
            return u'第%d次顶背离' % (x)
        elif x < 0:
            return u'第%d次底背离' % (-x)
        else:
            return u'无顶或底背离'

    for row in df.itertuples(index=False):
        obj = {}
        obj["title"] = u'%s板块(%s)于(%s)发现%s现象' % (row.sec_name, row.wind_code[:-3],
                                                 row.tday, _keywords(row.alertMACD))
        sqlt = sql + ' AND m.SID = %d WHERE f.tday="%s";' % (row.SID, row.tday)
        dft = pd.read_sql(sqlt, engine)
        if dft.empty:
            obj["content"] = u'本板块没有关注的股票'
        else:
            dft[u'重点股票'] = dft['sec_name'].str.cat(dft['wind_code'].str.slice(0, -3))
            dft[u'多空序列'] = dft.apply(_bullbear, axis=1)
            dft.rename(columns={'turn05': u'近期换手', 'turn520': u'远期换手',
                                'classes': u'相关概念'}, inplace=True)
            obj["content"] = dft[[u'重点股票', u'多空序列', u'近期换手', u'远期换手', u'相关概念']].T.to_json()
        array.append(obj)
        # print(array)
    return df


def plotKmacd(SID, thedate, engine):
    '''paint the candle graph with volume and MACD
    Parameters:
        SID:        int, SID of the sector
        thedate:    Timestamp/datetime, the date
        engine:     sqlalchemy engine
    return: fig object??
    '''
    # print("I am here")
    sector = pd.read_sql(u'SELECT wind_code,sec_name,classes FROM sectors \
                        WHERE SID=%d ' % (SID), engine).iloc[0]
    #    print("+++++++++++++++++++++++++++")
    #    print(sector)
    title = sector['classes'] + u'板块' + sector['sec_name'] + '(' + sector['wind_code'] + u')于' + thedate.strftime(
        '%Y%m%d') + u'发生'
    startday = thedate - pd.Timedelta('182 days')
    df = pd.read_sql(u'SELECT tday,OPEN,HIGH,LOW,CLOSE,VOLUME,MACD,alertMACD,alertREFD FROM sectorprice \
                        WHERE SID=%d AND tday >= \'%s\' \
                        ORDER BY tday' % (SID, startday), engine)
    #    print("+++++++++++++++++++++++++++")
    #    print(df)
    df.index = df.index + 1
    df['ind'] = df.index.values
    ohlc = df[["ind", "OPEN", "HIGH", 'LOW', "CLOSE"]].values
    volume = df['VOLUME'].values
    MACD = df['MACD'].values

    df1 = df.loc[df['tday'] < (thedate + pd.Timedelta('1 days'))]
    if df1['alertMACD'].iloc[-1] > 0:
        posidx = df1[df1['MACD'] < 0].index
        keyword = u'顶'
    elif df1['alertMACD'].iloc[-1] < 0:
        posidx = df1[df1['MACD'] > 0].index
        keyword = u'底'
    else:
        return -1
    if abs(df1['alertMACD'].iloc[-1]) > 1:
        title = title + u'真' + keyword + u'背离'
    else:
        title = title + u'假' + keyword + u'背离'
    pos1 = 0 if not len(posidx) else posidx[-1] + 1
    df1 = df.iloc[pos1:]
    df1 = df1.loc[df1['alertMACD'] != 0]
    peak_x = df1.index.values
    peak_y = df1['CLOSE'].values
    # print("here")
    df1 = df1.groupby('alertREFD').first()
    df1.reset_index(inplace=True)
    df1 = pd.merge(df1, df, left_on='alertREFD', right_on='tday', suffixes=['', '_1'])
    df1 = df1.reindex(pd.Index(np.arange(0, len(df1) - 0.5, 0.5)))
    line_x = df1[['ind', 'ind_1']].values.flatten()
    line_yp = df1[['CLOSE', 'CLOSE_1']].values.flatten()
    line_ym = df1[['MACD', 'MACD_1']].values.flatten()
    plt.ioff()
    matplotlib.rc('font', **{'family': 'sans-serif', \
                             'sans-serif': 'DengXian, DejaVu Sans, \
                             Bitstream Vera Sans, Lucida Grande, \
                             Verdana, Geneva, Lucid, Arial, \
                             Helvetica, Avant Garde, sans-serif'})
    matplotlib.rc('axes', **{'unicode_minus': False})
    matplotlib.style.use('dark_background')

    # N=len(df)
    # dates=df['tday'].tolist()
    # dates.insert(0,dates[0]-pd.Timedelta(1, unit='d'))
    # dates.append(dates[-1]+pd.Timedelta(1, unit='d'))
    # def format_date(x, pos=None):
    #     thisind = np.clip(int(x+0.5), 0, N+1)
    #     return dates[thisind].strftime('%Y-%m-%d')
    # fig = plt.figure()
    # ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1, axisbg='#07000d')
    # plt.title(title, {'color':'w', 'size':20})
    # ax1.axvspan(pos1,N,alpha=0.5)
    # candlestick_ohlc(ax1, ohlc, width=.8, colorup='#ff1717', colordown='#53c156') #K线
    # ax1.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
    # ax1.plot(peak_x, peak_y, '<', mfc=None, mec='w', mew=3, ms=8) 
    # ax1.plot(line_x,line_yp,color='gold',linewidth=2) 
    # ax1.grid(True, color='w',alpha=0.5)
    # plt.ylabel(u'股价和成交量')

    # ax1v = ax1.twinx()
    # ax1v.fill_between(df.index.values,0, volume, facecolor='#0079a3', alpha=0.3)
    # ax1v.axes.yaxis.set_ticklabels([])
    # ax1v.grid(False)
    # ax1v.set_ylim(0, 3*volume.max())

    # ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)
    # ax2.axvspan(pos1,N,alpha=0.5)
    # ax2.plot(df.index.values,MACD,color='w',linewidth=1, alpha=1)
    # ax2.plot(line_x,line_ym,color='gold',linewidth=2)
    # ax2.axhline(0, color='grey', linewidth=1,alpha=0.7)
    # ax2.grid(True, alpha=0.5)
    # plt.ylabel('MACD-DIF')

    # fig.autofmt_xdate()
    # plt.subplots_adjust(left=0.04, bottom=0.06, right=0.99, top=0.96, wspace=0.2, hspace=0)
    # figManager = plt.get_current_fig_manager()
    # figManager.window.showMaximized()
    # for row_num in range(df.shape[0]):
    #     print(row_num)
    # print(df.index)
    # print(df ** 2)
    # print(df.shape[0])
    # return
    print(df)

    # for row_num in range(df.shape[0]):
    # tmpList = []
    # for row_num in range(df.shape[0]):
    #     tmpList.append([df.ix[row_num, n*2], df.ix[row_num, n*2+1]])
    # objs[df.columns[n*2]+' / '+df.columns[n*2+1]] = [tmpList]
    # elif chartype == 2:
    #     print(df)
    #     objs = {}
    #     for n in range(int(df.shape[1] / 2)):
    #         tmpList = []
    #         for row_num in range(df.shape[0]):
    #             tmpList.append([df.ix[row_num, n*2], df.ix[row_num, n*2+1]])
    #         objs[df.columns[n*2]+' / '+df.columns[n*2+1]] = [tmpList]
    #     return json.dumps(objs)


def main():
    startdate = pd.datetime(2017, 1, 4).date()
    enddate = startdate + pd.Timedelta(1, unit='d')
    df = showMACDresult(startdate, enddate)
    # print(df)

    print(u'--------------TOTAL--------------')
    # print( df.itertuples(index=False) )
    # for row in df.itertuples(index=False):
    # print(row.SID,row.tday,engine)

    plotKmacd(240, pd.datetime(2017, 1, 5).date(), engine)


if __name__ == "__main__":
    main()
