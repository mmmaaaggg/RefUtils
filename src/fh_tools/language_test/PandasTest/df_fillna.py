import pandas as pd
import numpy as np
from datetime import date, datetime, timedelta
from math import isnan

weight = {
    's1': np.arange(10, 15.0, 1),
    's2': np.arange(10, 15.0, 1),
    's3': np.arange(10, 15.0, 1),
    's4': np.arange(10, 15.0, 1),
}
date_base = datetime.strptime('2016-1-1', '%Y-%m-%d').date()
day_1 = timedelta(days=1)
date_index = [date_base,
              date_base + day_1,
              date_base + day_1 * 2,
              date_base + day_1 * 3,
              date_base + day_1 * 4]
num_index = [0, 1, 2, 3, 4]
df1 = pd.DataFrame(weight, index=date_index)
df1['s1'][1] = np.nan
df1['s2'][1:3] = np.nan
df1['s3'][0:3] = np.nan
df1['s4'][2:5] = np.nan
print('df1:\n', df1)
print('df1.fillna(0):\n', df1.fillna(0))
print('df1.interpolate():\n', df1.interpolate())
print("df1.ffill().bfill():\n", df1.ffill().bfill())
print(((date_base + day_1) <= df1.index) & (df1.index <= (date_base + day_1 * 3)))
print(df1.iloc[((date_base + day_1) <= df1.index) & (df1.index <= (date_base + day_1 * 3))])

