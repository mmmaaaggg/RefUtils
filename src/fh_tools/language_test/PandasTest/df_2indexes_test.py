'''
主要用来测试双索引的情况下DataFrame能否进行合并
输出excel等操作
'''
import pandas as pd
import numpy as np

weight = {
    's1': np.random.random(3),
    's2': np.random.random(3),
    's3': np.random.random(3),
    's4': np.random.random(3),
    }
df1 = pd.DataFrame(weight, index=[['a', 'b', 'c'], ['h', 'i', 'j']])
print('DataFrame:df1\n', df1)
print("DataFrame:df1[['s1','s2']]\n", df1[['s1', 's2']])

df2 = pd.DataFrame(weight, index=[['k', 'l', 'm'], ['d', 'e', 'f']])
df_all = pd.concat([df1, df2])
print("pd.concat([df1,df2])\n", df_all)
df_all.to_excel('df_excel.xls')

pan = pd.Panel({"df1": df1, "df2": df2})
pan.to_excel('panel_excel.xls')
