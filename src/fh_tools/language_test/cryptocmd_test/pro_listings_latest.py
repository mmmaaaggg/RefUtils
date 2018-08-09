#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/8/1 8:31
@File    : only_test.py
@contact : mmmaaaggg@163.com
@desc    : 
"""
import requests
import pandas as pd


def get_price_latest():
    header = {
        'Content-Type': 'application/json',
        'X-CMC_PRO_API_KEY': 'f13a34ac-6460-4ffd-81fb-9805acf41902'
    }
    params = {
        # 'CMC_PRO_API_KEY': 'f13a34ac-6460-4ffd-81fb-9805acf41902',
        'limit': 5000,
        'start': 1
    }
    # https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?sort=market_cap&start=0&limit=10&cryptocurrency_type=tokens&convert=USD,BTC
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

    rsp = requests.get(url=url, params=params, headers=header)
    if rsp.status_code == 200:
        ret_dic = rsp.json()
        data_list = ret_dic['data']
        print('len(data_list):', len(data_list))

        data_dic_list = []
        for dic in data_list:
            data_dic = {}
            for key, val in dic.items():
                if key == 'quote':
                    for sub_key, sub_val in val['USD'].items():
                        data_dic[sub_key] = sub_val
                else:
                    data_dic[key] = val
            data_dic_list.append(data_dic)

        df = pd.DataFrame(data_dic_list)
    else:
        raise ValueError('获取数据异常 %d\n%s', rsp.status_code, rsp.content)

    return df


if __name__ == "__main__":
    from datetime import datetime
    df = get_price_latest()
    df.to_csv('latest_price_{0}.csv'.format(datetime.now().strftime('%y-%m-%d %H-%M-%S')))
