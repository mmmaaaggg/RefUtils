import numpy as np
import pandas as pd


data_list = np.random.randint(0, 70, 20)
print(data_list)
# 返回第一个大于50的数字所在位置
print(np.arange(len(data_list))[data_list > 50][0])
# 算法太复杂，而且效率很低，有没有简单点的
for n, val in enumerate(data_list):
    if val > 50:
        print(n)
        break

weight = {
    's1': np.random.random(6),
    's2': np.random.random(6),
    's3': np.random.random(6),
    's4': np.random.random(6),
}
df1 = pd.DataFrame(weight, index=['a', 'b', 'c', 'd', 'e', 'f'])
print(df1)
# s2 列，第一个大于 0.8 的行index值
