# -*- coding: utf-8 -*-
"""
Created on 2017/6/3
@author: MG
"""
import matplotlib.pyplot as plt
import pandas as pd

df = pd.DataFrame({'value': range(10),
              'group': [1, 1, 1, 2, 2, 2, 3, 3, 3, 3]})
# df['group'].plot(kind='bar', color=['r', 'g', 'b', 'r', 'g', 'b', 'r'])
colors = {1: 'r', 2: 'b', 3: 'g'}
df['value'].plot(kind='bar', color=[colors[i] for i in df['group']])
df['value'].plot(color='r')
plt.show()
