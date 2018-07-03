# -*- coding: utf-8 -*-
"""
Created on 2017/7/7
@author: MG
"""
import math
import matplotlib.pyplot as plt  # pycharm 需要通过现实调用 plt.show 才能显示plot
import pandas as pd


def linefit(x , y):
   N = float(len(x))
   sx,sy,sxx,syy,sxy=0,0,0,0,0
   for i in range(0,int(N)):
       sx  += x[i]
       sy  += y[i]
       sxx += x[i]*x[i]
       syy += y[i]*y[i]
       sxy += x[i]*y[i]
   a = (sy*sx/N -sxy)/( sx*sx/N -sxx)
   b = (sy - a*sx)/N
   if a==0:
       r=0
   else:
       r = abs(sy*sx/N-sxy)/math.sqrt((sxx-sx*sx/N)*(syy-sy*sy/N))
   return a,b,r

if __name__ == "__main__":
    file_name_list = ['29379.txt', '29433.txt', '29439.txt']

    data_df_all = None
    name_col_dic = None
    for filen_name in file_name_list:
        data_df = pd.read_csv(filen_name, sep=' ')
        if name_col_dic is None:
            name_col_dic = {col_name: [] for col_name in data_df.columns}
        data_df.rename(columns={col_name: col_name + ' on ' + filen_name for col_name in name_col_dic.keys()}, inplace=True)
        for key in name_col_dic.keys():
            name_col_dic[key].append(key + ' on ' + filen_name)
        if data_df_all is None:
            data_df_all = data_df
        else:
            data_df_all = pd.merge(data_df_all, data_df, how='inner', left_index=True, right_index=True)
        # data_df.plot()
        # print(data_df.shape)
        # print(data_df.head())
        # chg_df = (data_df.pct_change() +1).cumprod()
        # chg_df.plot()
    abr_dic = {}
    for key, col_names in name_col_dic.items():
        data_df_all[col_names].plot()
        for col_name in col_names:
            y = list(data_df_all[col_name])
            x = list(data_df_all.index)
            try:
                a, b, r = linefit(x, y)
                print("%s linefit result: y = %f x + %f y + %f" % (col_name, a, b, r))
                abr_dic[col_name] = (a, b, r)
            except:
                pass
    plt.show()

