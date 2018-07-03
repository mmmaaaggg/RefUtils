'''
主要用来测试双索引group的情况下DataFrame进行循环的操作
'''
import pandas as pd
import numpy as np

weight = {
    's1': np.random.random(8),
    's2': np.random.random(8),
    's3': np.random.random(8),
    's4': np.random.random(8),
    }
df1 = pd.DataFrame(weight, index=[['a', 'b', 'a', 'b', 'a', 'b', 'a', 'b'], ['h', 'h', 'h', 'h', 'i', 'i', 'i', 'i']]).reset_index()
print('DataFrame:df1\n', df1)
df_group = df1.groupby(['level_0', 'level_1'])
# print(df_group)
grouped_df_dic = dict(list(df_group))
#print(grouped_df_dic)
for key, data_df in grouped_df_dic.items():
    print(key, '\n', data_df)
# 无需 todict 在for items 直接 操作就可以
for key, data_df in df_group:
    print(key, '\n', data_df)

dfg = df1.groupby('level_0')
print("dfg.get_group('a'):\n", dfg.get_group('a'))