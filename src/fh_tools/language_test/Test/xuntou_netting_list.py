# -*- coding: utf-8 -*-
"""
Created on 2017/6/20
@author: MG
"""
import pandas as pd
import numpy as np
from datetime import date
BUY = 0
SELL = 1


def filter_holding_df(df, account_id):
    df_dic = dict(list(df.groupby('账号')))
    df_holding = df_dic[account_id]
    df_holding = df_holding[['名称', '可用数量']].rename(columns={'名称': '证券名称',
                                                                                '可用数量': '成分股数量'})
    return df_holding


def net_buy_sell(account_id, holding_csv_file_path, buying_csv_file_path, output_csv_file_path):
    """
    根据 持仓 及 买入 列表 整理出 轧差列表 生成到 输出文件 
    :param account_id: 账号
    :param holding_csv_file_path: 
    :param buying_csv_file_path: 
    :param output_csv_file_path: 
    :return: 
    """
    #  读 csv文件
    holding_df = pd.read_csv(holding_csv_file_path, index_col=2, encoding='GBK')
    holding_df = filter_holding_df(holding_df, account_id)
    buying_df = pd.read_csv(buying_csv_file_path, index_col=0, encoding='GBK')
    # outer join 两个表格
    tot_df = pd.merge(buying_df, holding_df, how='outer', left_index=True,
                      right_index=True)  # , suffixes=['buying', 'holding']

    # 将持仓及待买入股票进行轧差
    app_count_s = tot_df['数量']  # 申请买卖数量
    holding_count_s = tot_df['成分股数量'].apply(lambda x: x.strip('股') if type(x) == str else x)  # 持仓数量
    weight_s = tot_df["相对权重"]
    buy_sell_s = tot_df['方向']
    app_list = []
    for sec_code in tot_df.index:
        sec_code_str = '%06d' % sec_code
        if np.isnan(app_count_s[sec_code]):
            # 有持仓，没有对应买卖申请，卖出
            app_list.append({'代码': sec_code_str,
                             '名称': tot_df['证券名称'][sec_code],
                             '数量': holding_count_s[sec_code],
                             '相对权重': 0,
                             '方向': SELL,
                             })
        elif np.isnan(holding_count_s[sec_code]):
            # 无持仓，有对应买卖申请
            app_list.append({'代码': sec_code_str,
                             '名称': tot_df['名称'][sec_code],
                             '数量': app_count_s[sec_code],
                             '相对权重': 0,
                             '方向': BUY,
                             })
        else:
            # 有持仓，申请买入
            if buy_sell_s[sec_code] == str(BUY):
                net_app_count = app_count_s[sec_code] - holding_count_s[sec_code]
            else:
                net_app_count = -app_count_s[sec_code]
            if net_app_count > 0:
                # 加仓
                app_list.append({'代码': sec_code_str,
                                 '名称': tot_df['名称'][sec_code],
                                 '数量': abs(net_app_count),
                                 '相对权重': 0,
                                 '方向': BUY,
                                 })
            else:
                # 减仓
                app_list.append({'代码': sec_code_str,
                                 '名称': tot_df['名称'][sec_code],
                                 '数量': abs(net_app_count),
                                 '相对权重': 0,
                                 '方向': SELL,
                                 })

    new_app_df = pd.DataFrame(app_list)[['代码', '名称', '数量', '相对权重', '方向']].astype(
        {'方向': int, '相对权重': int, '数量': int})
    # print(new_app_df)
    new_app_df.to_csv(output_csv_file_path, index=False, encoding='GBK')
    print('%d data output' % new_app_df.shape[0])

if __name__ == "__main__":
    account_id = 81100364  # 81100682
    holding_csv_file_path = r"d:\Downloads\holding 2017-7-10.csv"
    buying_csv_file_path = r"d:\Downloads\EquityStrategy2017-07-11.csv"
    output_csv_file_path = r'd:\Downloads\讯投轧差交易 %d %s.csv' % (account_id, date.today())

    net_buy_sell(account_id, holding_csv_file_path, buying_csv_file_path, output_csv_file_path)
