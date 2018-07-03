import pandas as pd
import numpy as np
import xlrd
from datetime import datetime, date

file_path = r'd:\Downloads\善智净值20170331.xlsx'
data = xlrd.open_workbook(file_path) # 打开xls文件
fund_name_list = data.sheet_names()  # ["fund_sheet1"]
name_list = ['年化收益率', '年化波动率', '年化下行波动率', '最终净值', '最低净值', '最大回撤', '最长不创新高（周）', '夏普率', 'Sortino比率', '卡马比率', '盈亏比', '胜率',
             '统计周期最大收益', '统计周期最大亏损', '最大月收益', '最大月亏损']
output = pd.DataFrame(index=name_list)

RF = 0.02
start_date = datetime.strptime("2015-12-31", '%Y-%m-%d').date()
end_date = datetime.strptime("2017-12-31", '%Y-%m-%d').date()


def value2ret(X):
    Y = X / np.append(X[0], X[:-1]) - 1
    return Y


def SelectByDate(Data, starttime, endtime):
    newdata = Data[(Data.Date >= starttime) & (Data.Date <= endtime)]
    newdata = newdata.reset_index(drop=True)
    return newdata


for fund_name in fund_name_list:
    data_df = pd.read_excel(file_path, sheetname=fund_name, header=0).dropna()
    date_col_name = data_df.columns[0]
    data_col_name = data_df.columns[1]
    if type(data_df[date_col_name][0]) == str:
        print(fund_name)
        data_df[date_col_name] = data_df[date_col_name].apply(lambda x:datetime.strptime(x, '%Y/%m/%d').date())
    data_range = (start_date <= data_df[date_col_name]) & (data_df[date_col_name] <= end_date)
    data_df = data_df[data_range]
    data_df.set_index(date_col_name, inplace=True)
    data_df['pct'] = data_df[data_col_name].pct_change().fillna(0)
    data_df['ret'] = (1 + data_df['pct']).cumprod()
    time_fraction = data_df.index[-1] - data_df.index[0]

    ##basic indicators
    CAGR = data_df[data_col_name][data_df.index[-1]] ** (365 / time_fraction.days) - 1
    Vol = np.std(data_df.ret, ddof=1) * np.sqrt(50)
    DownSideVol = np.std(data_df.ret[data_df.ret < 0], ddof=1) * np.sqrt(50)
    WeeksNum = data_df.shape[0]
    WinRate = -np.mean(data_df.ret[data_df.ret > 0]) / np.mean(data_df.ret[data_df.ret < 0])
    WinRatio = len(data_df.ret[data_df.ret >= 0]) / len(data_df.ret)

    MinValue = min(data_df[data_col_name])
    FinalValue = data_df[data_col_name][data_df.index[-1]]
    MaxRet = max(data_df.ret)
    MinRet = min(data_df.ret)
    ##End of basic indicators

    ## max dropdown related
    data_df['mdd'] = data_df[data_col_name] / data_df[data_col_name].cummax() - 1
    mddsize = min(data_df.mdd)
    droparray = data_df.index[data_df.mdd == 0]
    mddweeks = max(pd.Series(droparray[1:]) - pd.Series(droparray[:-1])).days - 1
    ## End of max dropdown related


    ##High level indicators
    SharpeRatio = (CAGR - RF) / Vol
    SortinoRatio = (CAGR - RF) / DownSideVol
    CalMarRatio = CAGR / (-mddsize)
    ##End of High level indicators


    ## Natural month return 
    j = 1
    date_list = list(data_df.index)
    for i in range(len(date_list)):
        if i == 0:
            month_ret = pd.DataFrame([[date_list[i], data_df[data_col_name][i]]], columns=('Date', 'Value'))
        else:
            if date_list[i].month != date_list[i - 1].month:
                month_ret.loc[j] = [date_list[i - 1], data_df[data_col_name][i - 1]]
                j += 1
    month_ret.loc[j] = [date_list[-1], data_df[data_col_name][-1]]
    month_ret['ret'] = month_ret[data_col_name].pct_change().fillna(0)
    MaxMonRet = max(month_ret.ret)
    MinMonRet = min(month_ret.ret)
    ##End of Natural month return 

    variable = [CAGR, Vol, DownSideVol, FinalValue, MinValue, mddsize, mddweeks, SharpeRatio, SortinoRatio, CalMarRatio,
                WinRate, WinRatio, MaxRet, MinRet, MaxMonRet, MinMonRet]
    output[fund_name] = variable

output.to_excel(r"TestIndex.xlsx", 'Sheet1')
