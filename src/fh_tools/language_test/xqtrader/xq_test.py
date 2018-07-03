# -*- coding: utf-8 -*-
"""
Created on 2017/5/18
@author: MG
"""
import pandas as pd
from xqtrader_utils.stockbuyer import trade_xq_weighted

if __name__ == "__main__":
    # 使用之处首先配置 xq_conf.json文件 填写用户名，密码

    # 支持两种方式调用

    # 1）输入股票列表，默认等权重买入
    # trade_xq(['600123', '300123', '002778'])

    # 2）输入股票列表及对应权重 DataFrame
    stock_buy_df = pd.DataFrame([['600123', 0.2],
                                 ['300123', 0.3],
                                 ['000686', 0.4]])
    trade_xq_weighted(stock_buy_df, user='mmmaaaggg@163.com', password='', portfolio_code='ZH963277')
