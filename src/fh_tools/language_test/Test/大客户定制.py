import pandas as pd
import numpy as np
import xlrd
#from datetime import datetime
import datetime as dt


#path = r"D:\FH\作家\基金净值表\4月.xlsx"
path = r"D:\Downloads\鑫隆产品.xlsx"
data = xlrd.open_workbook(path) # 打开xls文件
fundnames = data.sheet_names()  # ["fund_sheet1"]

varnames = ['成立时间','年化收益率','年化波动率','年化下行波动率','最终净值','最低净值','最大回撤','最长不创新高（周）','夏普率','Sortino比率','卡马比率','盈亏比','胜率',
            '统计周期最大收益','统计周期最大亏损','最大月收益','最大月亏损']
output = pd.DataFrame(index=varnames)

RF = 0.02 #无风险利率
freq = 50 #日数据250，周数据50
#starttime = pd.tslib.Timestamp("2011-12-31") 
#endtime = pd.tslib.Timestamp("2017-12-31") 
starttime = dt.datetime.strptime("2011-12-31", '%Y-%m-%d').date()#开始时间
endtime = dt.datetime.strptime("2017-12-31", '%Y-%m-%d').date()#结束时间

def value2ret(X):
    Y = X/np.append(X[0],X[:-1])-1
    return(Y)


def SelectByDate(Data,starttime,endtime):
    newdata = Data[(Data.Date>=starttime)  & (Data.Date <= endtime)]
    newdata = newdata.reset_index(drop = True)
    return(newdata)
    
for fundname in fundnames:
    data = pd.read_excel(path,sheetname=fundname,header=0)
    data.columns = ['Date','Value']
    #data = data.fillna(method = 'bfill')
    date_col_name = data.columns[0]
    value_col_name = data.columns[1]

    if type(data[date_col_name][0]) == str:
        print(fundname)
        datetype = data[date_col_name][0][4]
        if(datetype == '/'):
            data[date_col_name] = data[date_col_name].apply(lambda x:dt.datetime.strptime(x, '%Y/%m/%d').date())
        elif(datetype == '-'):
            data[date_col_name] = data[date_col_name].apply(lambda x:dt.datetime.strptime(x, '%Y-%m-%d').date())
        elif(datetype == '.'):
            data[date_col_name] = data[date_col_name].apply(lambda x:dt.datetime.strptime(x, '%Y.%m.%d').date())
        else:
            data[date_col_name] = data[date_col_name].apply(lambda x:dt.datetime.strptime(x, '%Y%m%d').date())
    if type(data[date_col_name][0]) == np.int64 :
        data[date_col_name] = data[date_col_name].apply(lambda x:dt.datetime.strptime(str(x), '%Y%m%d').date())

            

    data = SelectByDate(data,starttime,endtime)
    data.Value = data.Value/data.Value[0]
    #data['ret'] = value2ret(data.Value)
    data['ret'] = data.Value.pct_change().fillna(0)
    time_fraction = data.Date[data.index[-1]] - data.Date[data.index[0]]
    time_fraction = 365/time_fraction.days
    
    ##basic indicators
    CAGR = data.Value[data.index[-1]] ** time_fraction - 1
    Vol = np.std(data.ret,ddof=1)* np.sqrt(freq)
    DownSideVol=np.std(data.ret[data.ret<0],ddof = 1)*np.sqrt(freq)
    WeeksNum = data.shape[0]
    WinRate=-np.mean(data.ret[data.ret>0]) / np.mean(data.ret[data.ret<0])
    WinRatio=len(data.ret[data.ret>=0])/len(data.ret)
    
    MinValue = min(data.Value)
    FinalValue = data.Value[data.index[-1]]
    MaxRet = max(data.ret)
    MinRet = min(data.ret)
    ##End of basic indicators
    

    ## max dropdown related
    data['mdd'] = data.Value / data.Value.cummax() -1
    mddsize = min(data.mdd)
    droparray =  pd.Series(data.index[data.mdd==0])
    if(len(droparray) == 1):
        mddweeks = len(data.mdd)
    else:
        if(float(data.Value[droparray.tail(1)])>float(data.Value.tail(1))):
            droparray = droparray.append(pd.Series(data.index[-1]),ignore_index=True)
        mddweeks = max(droparray.diff().dropna())-1
    ## End of max dropdown related
    
    
    ##High level indicators
    SharpeRatio=(CAGR-RF)/Vol
    SortinoRatio=(CAGR-RF)/DownSideVol
    CalMarRatio=CAGR/(-mddsize)
    ##End of High level indicators
    
    
    ## Natural month return 
    j = 1
    for i in data.index:
        if(i==0):
            month_ret = pd.DataFrame([[data.Date[i],data.Value[i]]],columns=('Date','Value'))
        else:
            if((data.Date[i].month) != (data.Date[i-1].month)):
                month_ret.loc[j] = [data.Date[i-1],data.Value[i-1]]
                j+=1
    month_ret.loc[j] = [data.Date[data.index[-1]],data.Value[data.index[-1]]]
    month_ret['ret'] = value2ret(month_ret.Value)
    MaxMonRet = max(month_ret.ret)
    MinMonRet = min(month_ret.ret)
    ##End of Natural month return 

    if isinstance(data.Date[0],dt.date):
        BeginDate = data.Date[0]
    else:
        BeginDate = data.Date[0].date()
    variable = [BeginDate,CAGR,Vol,DownSideVol,FinalValue,MinValue,mddsize,mddweeks,SharpeRatio,SortinoRatio,CalMarRatio,WinRate,WinRatio,MaxRet,MinRet,MaxMonRet,MinMonRet]
    output[fundname] = variable

output.to_excel(r"D:\Downloads\鑫隆产品指标.xlsx")
