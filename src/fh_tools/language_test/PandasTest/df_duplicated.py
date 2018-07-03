# -*- coding: utf-8 -*-
"""
Created on 2017/4/6
@author: MG
"""
import pandas as pd
import numpy as np

weight = {
    's1': ['d1', 'd2', 'd2', 'd4', 'd5', 'd6'],
    's2': np.random.random(6),
    's3': np.random.random(6),
    's4': np.random.random(6),
}
df1 = pd.DataFrame(weight, index=['a', 'b', 'c', 'c', 'e', 'f'])
print(df1)
print(df1.duplicated('s1'))