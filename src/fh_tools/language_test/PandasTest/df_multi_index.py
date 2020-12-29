#! /usr/bin/env python3
"""
@author  : MG
@Time    : 2020/12/30 上午3:57
@File    : df_concat.py
@contact : mmmaaaggg@163.com
@desc    : DataFrame concat with key 会导致index 被group 输出excel后会不方便进行整理排序等操作,因此想办法去除index上的group
"""
import pandas as pd

df1 = pd.DataFrame(
    {
        'a': [1, 1, 1, 1, 2, 2, 2, 2],
        'b': [1, 1, 2, 2, 3, 3, 4, 4],
        'data': [1, 2, 3, 4, 5, 6, 7, 8],
    }
).set_index(['a', 'b'])
#      data
# a b
# 1 1     1
#   1     2
#   2     3
#   2     4
# 2 3     5
#   3     6
#   4     7
#   4     8
df1.reset_index()
#    a  b  data
# 0  1  1     1
# 1  1  1     2
# 2  1  2     3
# 3  1  2     4
# 4  2  3     5
# 5  2  3     6
# 6  2  4     7
# 7  2  4     8

if __name__ == "__main__":
    pass
