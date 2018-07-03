# -*- coding: utf-8 -*-
"""
Created on 2017/4/10
@author: MG
"""
import pandas as pd
from datetime import datetime, timedelta
import numpy as np


weight = {
    's1': np.random.random(6),
    's2': np.random.random(6),
    's3': np.random.random(6),
    's4': np.random.random(6),
}
date_base = datetime.strptime('2016-1-1', '%Y-%m-%d').date()
day_1 = timedelta(days=1)
date_index = [date_base,
              date_base + day_1,
              date_base + day_1 * 2,
              date_base + day_1 * 3,
              date_base + day_1 * 4,
              date_base + day_1 * 5]
df1 = pd.DataFrame(weight, index=[date_index, ['a', 'b', 'c', 'd', 'e', 'f']])
print(df1)
p1 = df1.to_panel()
print(p1)
