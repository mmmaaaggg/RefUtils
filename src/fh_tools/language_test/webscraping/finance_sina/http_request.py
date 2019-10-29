# -*- coding: utf-8 -*-
"""
Created on 2018/2/7
@author: MG
获取 新浪财经实时行情的 OHLC 例如 http://finance.sina.com.cn/fund/quotes/512760/bc.shtml
"""
import pandas as pd
import logging

import requests

logger = logging.getLogger()

def fetch_data(stock_code_list, output_path):
    """
    从新浪财经抓取实时行情 OHLC，参考网址：http://finance.sina.com.cn/fund/quotes/512760/bc.shtml
    :param stock_code_list: 股票代码
    :param output_path: 输出文件路径
    :return: 
    """
    data_list = []
    for code in stock_code_list:
        url_str = f"http://hq.sinajs.cn/?list={code}"
        try:
            kv = {"user-agent": "Mozilla/5.0",
                  'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8,la;q=0.7",
                  }
            r = requests.get(url_str, headers=kv)
            r.raise_for_status()
            # 如果状态不是200，引发 HTTPError 异常
            # r.encoding = r.apparent_encoding
            data = r.text
            if data is None or len(data) <= 30:
                continue
            # print(data)
            hq_data = data.split(sep='"')[1]
            hq_s = pd.Series(hq_data.split(',')[:9],
                             index=['name', 'open', 'high', 'low', 'close', '5', '6', '7', 'vol'])
            hq_s['code'] = code
            data_list.append(hq_s)
        except requests.HTTPError:
            return None

    data_df = pd.DataFrame(data_list)[['code', 'name', 'open', 'high', 'low', 'close', 'vol']]
    print(data_df)
    data_df.to_csv(output_path, index=False)
    return data_df


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s: %(levelname)s [%(name)s] %(message)s')
    stock_code_list = ['sh512760']
    file_path = 'output.csv'
    fetch_data(stock_code_list, file_path)
