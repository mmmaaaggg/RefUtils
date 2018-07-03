# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 12:38:20 2017

@author: forise
"""
import pandas as pd
import WindPy as WP
import numpy as np
import time
import datetime

WP.w.start()
acc_3 = 'W106095802401'
# acc_3 = 'W2246500401'
account = [acc_3]
password = ['123456'] * len(account)

trade_logon = WP.w.tlogon("0000", "0", account, password, "SHSZ")
minutes_waiting = 1
position_control = [1] * len(account)
min_trade_amount = 10000
signal_path = r'D:\FH\SimTrade\ma\2017.04.06_MG.csv'
signal_m = pd.read_csv(signal_path)
signal_m.columns = ['code']


def trade_stocks(signals_in, position_control, logon_id_in, min_trade_amount):
    '''
    Function:trade stocks according to signals_in and position_control for the logon_id_in account
    signals_in:DataFrame,code:wind code
    position_control: position ratio
    '''
    position_info = WP.w.tquery("Position", "LogonId=" + str(logon_id_in))
    if len(position_info.Data) == 3:  # no position exists
        position_info = pd.DataFrame(columns=['code', 'shares', 'shares_balance'])
    else:  # shares_balance stands for old position;shares_new stands for new position today;shares_balance+shares_new is the total current position
        position_info = pd.DataFrame({'code': position_info.Data[0], 'shares_balance': position_info.Data[2],
                                      'shares_new': position_info.Data[5]})
        position_info['shares'] = position_info.shares_balance + position_info.shares_new

    # current account info
    account_info = WP.w.tquery("Capital", "LogonId=" + str(logon_id_in))
    total_asset = account_info.Data[5][0]
    aim_position = position_control * total_asset

    # current price
    stock_code_list = signals_in.code.tolist()
    data = WP.w.wsq(stock_code_list, "rt_time,rt_susp_flag,rt_high_limit,rt_last,rt_trade_status")
    stock_df = pd.DataFrame(data.Data, index=data.Fields, columns=data.Codes).T
    stock_code_list = list(stock_df.index[stock_df['RT_HIGH_LIMIT'] > stock_df['RT_LAST']])
    stock_code_count = len(stock_code_list)
    price = stock_df['RT_LAST'][stock_code_list]
    # price = pd.Series(WP.w.wsq(stock_code_list, 'rt_last').Data[0], name='price')
    # shares to buy using current price
    # equal weighted portfolio is used for simplicity
    aim_shares = pd.Series(
        (aim_position / price / stock_code_count).map(lambda x: np.floor(x / 100) * 100).tolist(),
        name='aim_shares')

    # calculate position adjustment
    # merge and create a data frame
    AIM = pd.concat([stock_code_list, price, aim_shares], axis=1, join='outer')
    AIM = pd.merge(AIM, position_info, on='code', how='outer')
    AIM.fillna(0, inplace=True)
    AIM['adjust'] = AIM.aim_shares - AIM.shares
    AIM = AIM.where(~np.isinf(AIM.adjust), 0)

    AIM.price = pd.Series(WP.w.wsq(AIM.code.tolist(), 'rt_last').Data[0], name='price')
    AIM_new = AIM[abs(AIM.adjust * AIM.price) > min_trade_amount]
    buy_list = AIM_new[AIM_new.adjust > 0]
    sell_df = AIM_new[AIM_new.adjust < 0]

    sell_df.adjust = np.minimum(-sell_df.adjust, sell_df.shares_balance)
    sell_df = sell_df[sell_df.adjust > 0]

    # trade stocks
    if len(sell_df) > 0:
        stock_code_s = get_stock_noHL(sell_df.code.tolist())
        sell_df_indexed = sell_df.set_index('code')
        sell_df_indexed = sell_df_indexed.loc[stock_code_s]

        WP.w.torder(sell_df_indexed.index.tolist(), "Sell", (sell_df_indexed.price).tolist(), sell_df_indexed.adjust.tolist(),
                    "OrderType=LMT;LogonID=" + str(logon_id_in))  # 限价
    if len(buy_list) > 0:
        WP.w.torder(buy_list.code.tolist(), "Buy", (buy_list.price).tolist(), buy_list.adjust.tolist(),
                    "OrderType=LMT;LogonID=" + str(logon_id_in))  # 限价


def get_stock_noHL(stock_code_list):
    # 获取未涨停的股票的列表及对应价格
    data = WP.w.wsq(stock_code_list, "rt_time,rt_susp_flag,rt_high_limit,rt_last,rt_trade_status")
    stock_df = pd.DataFrame(data.Data, index=data.Fields, columns=data.Codes).T
    stock_code_s = pd.Series(stock_df.index[stock_df['RT_HIGH_LIMIT'] > stock_df['RT_LAST']], name='code')
    # stock_code_count = len(stock_code_s)
    # price_s = stock_df['RT_LAST'][stock_code_s]
    return stock_code_s


def calcel_order(logon_id_in):
    '''
    parameters:
        logon_id_in:int, logonIDs 
    '''
    order_in = WP.w.tquery('Order', "LogonId=" + str(logon_id_in))
    for i in range(len(order_in.Data[0])):
        WP.w.tcancel(order_in.Data[0][i], LogonID=logon_id_in)


def trading_log(path_in, logonID_in, account_in):
    for i in range(len(logonID_in)):
        trade_info = WP.w.tquery("Trade", "LogonId=" + str(logonID_in[i]))
        trade_log = pd.DataFrame({trade_info.Fields[3]: trade_info.Data[3], trade_info.Fields[4]: trade_info.Data[4],
                                  trade_info.Fields[5]: trade_info.Data[5], trade_info.Fields[10]: trade_info.Data[10],
                                  trade_info.Fields[11]: trade_info.Data[11]})
        trade_log.to_csv(path_in + '\\' + account_in[i] + '_' + datetime.date.today().strftime('%Y%m%d'))


def log_out(logonID_in):
    for i in range(len(logonID_in)):
        WP.w.tlogout(LogonID=str(logonID_in[i]))


def MultiAccountTrading(logonID_in, signal_dic_in, position_control_in, minutes_waiting_in, min_trade_amount):
    '''
    parameters:
        logonID_in:list, logonIDs 
        signal_dic_in:dictionary of DataFrame, which contain signal list 'code'
        position_control_in:list, position control ratio for each account
        minutes_waiting_in:double, time interval before calceling old order and trading again 
    '''
    while (datetime.datetime.now().hour < 15):
        for i in range(len(logonID_in)):
            trade_stocks(signal_dic_in[i], position_control_in[i], logonID_in[i], min_trade_amount)
        time.sleep(60 * minutes_waiting_in)
        for i in range(len(logonID_in)):
            calcel_order(logonID_in[i])


logonIDs = trade_logon.Data[0]
signal_dic = {0: signal_m}
account_num = 1
MultiAccountTrading(logonIDs[:account_num], signal_dic, position_control[:account_num], minutes_waiting,
                    min_trade_amount)
