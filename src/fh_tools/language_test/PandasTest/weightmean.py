# -*- coding:utf-8 -*-
'''
Created on 2016年12月23日

@author: Family
'''
import pandas as pd
import numpy as np
aaa = ['a']
aaa.extend(list(range(6)))
mapping = {
    's1':'a',
    's2':'a',
    's3':'b',
    's4':'b',
    }
print('mapping')
print(mapping)
# data = {
#     's1':np.random.rand(6),
#     's2':np.random.rand(6),
#     's3':np.random.rand(6),
#     's4':np.random.rand(6),
#     }
weight = {
    's1':list(range(6)),
    's2':list(range(1, 7)),
    's3':[6, 6, 6, 6, 6, 6],
    's4':[0, 0, 0, 0, 0, 0],
    }
# dfdata = pd.DataFrame(data)
# dfdata_g = dfdata.groupby(mapping, axis=1)
dfweight = pd.DataFrame(weight)
dfweight = (dfweight.T / dfweight.sum(axis=1)).T
print('weight:')
print(dfweight)

dfweight_g = dfweight.groupby(mapping, axis=1).sum()
print('dfweight_g:')
print(dfweight_g)

dfweight2 = dfweight.copy()
dfweight2[dfweight2<=0.2]=0
print('dfweight2')
print(dfweight2)
dfweight2_g = dfweight2.groupby(mapping, axis=1).sum()
dfweightchange = dfweight_g / dfweight2_g
dfweightchange[np.isinf(dfweightchange)]=0
print('dfweightchange')
print(dfweightchange)

dfweight3 = dfweight.copy()
# dfweight3.loc[1, 's3'] = np.nan
dfweight3['s3'] = [1, 2, np.nan, 3, 4, 5]
print('dfweight mean with nan')
print(dfweight3.mean())