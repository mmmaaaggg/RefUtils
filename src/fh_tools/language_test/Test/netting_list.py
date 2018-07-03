# -*- coding: utf-8 -*-
"""
Created on 2017/6/20
@author: MG
"""
import pandas as pd
import numpy as np
from datetime import date

product_code_stock = '342'
product_code_index = '343'
holding_df = pd.read_excel(r"d:\Downloads\alpha1_20170623_092752.xls", index_col=0)
buying_df = pd.read_excel(r"d:\Downloads\SectorRotation2017-06-23(1).xlsx", index_col=0)

tot_df = pd.merge(buying_df, holding_df, how='outer', left_index=True,
                  right_index=True)  # , suffixes=['buying', 'holding']
print(tot_df)

app_count_s = tot_df['委托数量']
holding_count_s = tot_df['成分股数量']
buy_sell_s = tot_df['买卖方向']
app_list = []
for sec_code in tot_df.index:
    sec_code_str = '%06d' % sec_code
    if np.isnan(app_count_s[sec_code]):
        # 有持仓，没有对应买卖申请
        app_list.append({'证券代码': sec_code_str,
                         '委托数量': holding_count_s[sec_code],
                         '买卖方向': '卖出',
                         '开平标志': 0,
                         '价格策略': '自动',
                         '产品': product_code_stock,
                         })
    elif np.isnan(holding_count_s[sec_code]):
        # 无持仓，有对应买卖申请
        app_list.append({'证券代码': sec_code_str,
                         '委托数量': app_count_s[sec_code],
                         '买卖方向': buy_sell_s[sec_code],
                         '开平标志': tot_df['开平标志'][sec_code],
                         '价格策略': tot_df['价格策略'][sec_code],
                         '产品': str(int(tot_df['产品'][sec_code])),
                         })
    else:
        # 有持仓，申请买入
        if buy_sell_s[sec_code] == '买入':
            net_app_count = app_count_s[sec_code] - holding_count_s[sec_code]
        else:
            net_app_count = -app_count_s[sec_code]
        if net_app_count > 0:
            # 加仓
            app_list.append({'证券代码': sec_code_str,
                             '委托数量': net_app_count,
                             '买卖方向': '买入',
                             '开平标志': tot_df['开平标志'][sec_code],
                             '价格策略': tot_df['价格策略'][sec_code],
                             '产品': str(int(tot_df['产品'][sec_code])),
                             })
        else:
            # 减仓
            app_list.append({'证券代码': sec_code_str,
                             '委托数量': -net_app_count,
                             '买卖方向': '卖出',
                             '开平标志': tot_df['开平标志'][sec_code],
                             '价格策略': tot_df['价格策略'][sec_code],
                             '产品': str(int(tot_df['产品'][sec_code])),
                             })

new_app_df = pd.DataFrame(app_list)[['证券代码', '委托数量', '买卖方向', '开平标志', '价格策略', '产品']]
print(new_app_df)
new_app_df.to_excel(r'd:\Downloads\SectorRotation_Netting%s.xlsx' % date.today(), index=False)
