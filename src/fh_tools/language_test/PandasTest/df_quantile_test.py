# -*- coding: utf-8 -*-
"""
Created on 2017/10/22
@author: MG
"""
import pandas as pd
import numpy as np
weight = {
    's1': [1, 2, 3, 4, 5],
    's2': [1, 2, 3, 4, np.nan],
    's3': [1, 2, np.nan, 4, 5],
    's4': [np.nan, 2, 3, 4, 5],
    }
df = pd.DataFrame(weight)
print(df.quantile([1/3, .5, .75]))