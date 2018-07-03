# -*- coding: utf-8 -*-
"""
Created on 2017/11/1
@author: MG
"""

from datetime import date, datetime, timedelta
import pandas as pd
import numpy as np
from math import isnan

weight = {
    's1': np.random.random(6),
    's4': np.random.random(6),
    's3': np.random.random(6),
    's2': np.random.random(6),
}
date_base = datetime.strptime('2016-1-1', '%Y-%m-%d').date()
day_1 = timedelta(days=1)
date_index = [date_base,
              date_base + day_1,
              date_base + day_1 * 2,
              date_base + day_1 * 3,
              date_base + day_1 * 4,
              date_base + day_1 * 5]
df1 = pd.DataFrame(weight, index=['a', 'b', 'c', 'd', 'e', 'f'])
print(df1)
print("*" * 20, '\n')

from functools import reduce
def reduce_list(funx, data_list, initial=None):
    result_list = []
    def reduce_func(x, y):
        # print(x,y)
        result = funx(x, y)
        result_list.append(result)
        return result
    if initial is None:
        reduce(reduce_func, data_list)
    else:
        reduce(reduce_func, data_list, initial)
    return result_list
reduce_list(lambda x,y:(x+y)/2, range(10))


def apply_func(x: pd.Series):
    print(x)
    print("*" * 10)
    return x
print('df1_apply = df1.apply(apply_func, reduce=False)')
df1_apply = df1.apply(apply_func, reduce=False)
print("df1_apply")
print(df1_apply)

print("res_list = reduce_list(lambda x,y: x if x > y else y, df1['s1'], df1['s1'].iloc[0])")
res_list = reduce_list(lambda x,y: x if x > y else y, df1['s1'], df1['s1'].iloc[0])
print(res_list, '\n')

print("res_list = df1.apply(lambda x: reduce_list(lambda x,y: x if x > y else y, x, x.iloc[0]))")
res_list = df1.apply(lambda x: reduce_list(lambda x,y: x if x > y else y, x, x.iloc[0]))
print(res_list, '\n')

print("*" * 20)
print(df1)


def _calc_mdd_4_drawback_analysis(pair, y):
    """
    此函数仅供 drawback_analysis 使用
    用于计算最大回撤使用
    :param pair: 
    :param y: 
    :return: 
    """
    max_y_last = pair[0]
    max_y = max_y_last if max_y_last > y else y
    mdd_last = pair[1]
    keep_max = pair[2]
    dd = y / max_y -1
    if keep_max:
        mdd = dd if dd < mdd_last else mdd_last
    else:
        mdd = dd
    return max_y, mdd, keep_max


keep_max = False
print("mdd_df = df1.apply(lambda xx: [rr[1] for rr in reduce_list(_calc_mdd_4_drawback_analysis, xx, (xx.iloc[0], 0, %s))])" % keep_max)
# mdd_df = df1.apply(lambda xx: [rr[1] for rr in reduce_list(calc_mdd, xx, (xx.iloc[0], 0))])
mdd_df = df1.apply(lambda xx: [rr[1] for rr in reduce_list(_calc_mdd_4_drawback_analysis, xx, (xx.iloc[0], 0, keep_max))])
print(mdd_df, '\n')

keep_max = True
print("mdd_df = df1.apply(lambda xx: [rr[1] for rr in reduce_list(_calc_mdd_4_drawback_analysis, xx, (xx.iloc[0], 0, %s))])" % keep_max)
mdd_df = df1.apply(lambda xx: [rr[1] for rr in reduce_list(_calc_mdd_4_drawback_analysis, xx, (xx.iloc[0], 0, keep_max))])
print(mdd_df, '\n')
