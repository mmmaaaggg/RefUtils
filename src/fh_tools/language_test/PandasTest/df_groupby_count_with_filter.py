"""
@author  : MG
@Time    : 2020/12/29 16:34
@File    : df_groupby_count_with_filter.py
@contact : mmmaaaggg@163.com
@desc    : 用于
"""
import numpy as np
import pandas as pd

weight = {
    'g': [1, 1, 1, 1, 2, 2, 2, 2],
    's1': np.random.random(8),
    's2': np.random.random(8),
    's3': np.random.random(8),
    's4': np.random.random(8),
}
df1 = pd.DataFrame(weight)
df1.groupby('g').aggregate(lambda x: sum(x > 0.5))

if __name__ == "__main__":
    pass
