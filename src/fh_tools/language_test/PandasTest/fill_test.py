# -*- coding: utf-8 -*-
"""
Created on 2017/6/1
@author: MG
"""

from datetime import date, datetime, timedelta
import pandas as pd
import numpy as np
from math import isnan
import numpy as np

weight = {
    's1': np.random.random(6),
    's2': [np.nan, 10, 9, np.nan, 7, np.nan],
    's3': [11, 10, 9, np.nan, 7, np.nan],
    's4': [np.nan, 10, 9, np.nan, 7, 6],
}
df1 = pd.DataFrame(weight, index=['a', 'b', 'c', 'd', 'e', 'f'])
print(df1)


class DataFrame(pd.DataFrame):

    def interplolate_inner(self, columns=None, inplace=False):
        if columns is None:
            columns = list(self.columns)
        data = self if inplace else self.copy()
        for col_name in columns:
            index_not_nan = data.index[~np.isnan(data[col_name])]
            index_range = (min(index_not_nan), max(index_not_nan))
            # data[col_name][index_range[0]:index_range[1]].interpolate(inplace=True)
            data[col_name][index_range[0]:index_range[1]] = data[col_name][index_range[0]:index_range[1]].interpolate()
        # print(data)
        if ~inplace:
            return data
print(DataFrame.interplolate_inner(df1))
