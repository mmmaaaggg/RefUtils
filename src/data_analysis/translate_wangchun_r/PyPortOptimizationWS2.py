# Load Data #
  # Load Code (csv)
  # Load OHLCV (sqlite db)
  # Load FV (csv)
  # Load Beta (sqlite db)
  # Load Equity SectorClassification (sqlite db)
  # Load EquityIndex Constitutes Info and Convert into Daily Frequency (sqlite db)
  
# Data Preparation
  # EquityIndex Sector Constitutes Info

# Run loop for each trading day t:
  # 1. at time t determine which stocks to hold for t+1: index_jy 
  # 2. compute covariance matrix (corrected for zero diagonal term) and sector-wise expected return
  # 3. run Portfolio Optimization: Constrained_OneStep_OptimFunc5() and retrieve results for Wopt[t+1,index_jy]

# Constrained_OneStep_OptimFunc5.py
  # 1. Prepare for X_sector (sector constraint matrix) and X_style(Size and Beta constraint matrix) at each trading day
  # 2. Run Optimization according to selected RiskMeasure
    # Risk_Adjusted_Return:    Constrained_MultiFactorModel_OptimFunc3()     
    # Risk_Parity:             Constrained_MultiFactorModel_OptimFunc5()           
    # Minimum_Tail_Dependent:  Constrained_MultiFactorModel_OptimFunc6()
    # Minimum_Variance:        Constrained_MultiFactorModel_OptimFunc3()
    # CVaR:                    Constrained_MultiFactorModel_OptimFunc7()


# Load Data #

import pandas as pd
import numpy as np
import cvxopt as cvx
import sqlite3
import os

   # Load Code #

file_path=r'D:\Rwork\AlphaStrategy\Rfiles\FuJuCode2.csv'
Code=pd.read_csv(file_path)["Code"]

   # Load OHLCV
conn=sqlite3.connect("D:/Rwork/AlphaStrategy/Data/DataBase/DB_FuJuDailybar.db")
df=pd.read_sql_query("SELECT * FROM X000001",conn)
def tables_in_sqlite_db(conn):
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [
        v[0] for v in cursor.fetchall()
        if v[0] != "sqlite_sequence"
    ]
    cursor.close()
    return tables

tables=tables_in_sqlite_db(conn)
n=len(tables)
codeX=np.zeros(n)

T=df.shape[0]
Open=np.zeros(shape=(T,n))
High=np.zeros(shape=(T,n))
Low=np.zeros(shape=(T,n))
Close=np.zeros(shape=(T,n))
Volume=np.zeros(shape=(T,n))
LiquidSize=np.zeros(shape=(T,n))
Size=np.zeros(shape=(T,n))
for i in range(0,(n-1)):
 A=pd.DataFrame(pd.read_sql_query("SELECT * FROM "+tables[i],conn))
 Open[:,i]=A["Open"]   # A.Open
 High[:,i]=A["High"]
 Low[:,i]=A["Low"]
 Close[:,i]=A["Close"]
 LiquidSize[:,i]=A["LiquidSize"]
 Size[:,i]=A["Size"]
 Volume[:,i]=A["Volume"]

LogClose=np.log(Close)
CC=np.zeros(shape=(T,n))
LogCC=np.zeros(shape=(T,n))
for i in range(0,(n-1)): 
 CC[1:T,i]=Close[1:T,i]/Close[0:(T-1),i]-1
 LogCC[1:T,i]=LogClose[1:T,i]-LogClose[0:(T-1),i]

Open=pd.DataFrame(Open).fillna(0)
High=pd.DataFrame(High).fillna(0)
Low=pd.DataFrame(Low).fillna(0)
Close=pd.DataFrame(Close).fillna(0)
LogClose=pd.DataFrame(LogClose).fillna(0)
Size=pd.DataFrame(Size).fillna(0)
Volume=pd.DataFrame(Volume).fillna(0)
LiquidSize=pd.DataFrame(LiquidSize).fillna(0)
CC=pd.DataFrame(CC).fillna(0)
LogCC=pd.DataFrame(LogCC).fillna(0)

  # Load FV
file_path = r'D:/Rwork/AlphaStrategy/Data/DataHis/equal_weighted.csv'
df=pd.read_csv(file_path,index_col=[0])
FV=df.fillna(-100)

  # Load Beta
file_path=r"D:/Rwork/AlphaStrategy/Graph/StrategyResult/EquityCurve_Beta.csv"
Beta=pd.read_csv(file_path,index_col=[0])
Beta=pd.DataFrame(Date).join(Beta)
Beta=Beta.fillna(0)

  # Load SectorClassification
conn=sqlite3.connect("D:/Rwork/AlphaStrategy/Data/DataBase/DB_SectorClassification.db")
df=pd.read_sql_query("SELECT * FROM X000001",conn)
Date=pd.to_datetime(df.Date)
def tables_in_sqlite_db(conn):
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [
        v[0] for v in cursor.fetchall()
        if v[0] != "sqlite_sequence"
    ]
    cursor.close()
    return tables

tables=tables_in_sqlite_db(conn)
T=df.shape[0]
n=len(tables)  
SectorClass=np.zeros(shape=(T,n))
for i in range(0,(n-1)):
  data=pd.DataFrame(pd.read_sql_query("SELECT * FROM "+tables[i],conn))
  SectorClass[:,i]=data["TYPE_ID"]  #data.Type_ID

SectorClass=pd.DataFrame(SectorClass)
SectorClass.columns=Code

SectorClass2=SectorClass.applymap(lambda x: str(int(x))[:8])
SectorU=[x for x in set(SectorClass2.to_numpy().flatten()) if x != '0']
SectorU.sort()
nsector=len(SectorU)

  # Load EquityIndex Constitutes Info and Convert into Daily Frequency
from collections import OrderedDict
folder_path=r'D:/Rwork/AlphaStrategy/Data/DataHis/DataConsDataYes/ZZ500'
Year=Date.dt.year
Month=Date.dt.month
files=os.listdir(folder_path)
files.sort()
nfile=len(files)
cons_dic=OrderedDict()
from_n=23
for i in range(23,(nfile-1)):
  df=pd.read_csv(folder_path+"/"+files[i],index_col=0,encoding='GBK')
  del df['Date']
  if i<(nfile-1):
    file_name_year=int(files[i+1][4:8])
    file_name_month=int(files[i+1][9:11])
    indexs=np.where((Year==file_name_year) | (Month==file_name_month))[0]
  if i==(nfile-1):
    file_name_year=int(files[i][4:8])
    file_name_month=int(files[i][9:11])
    indexs=np.where((Year==file_name_year) | (Month==file_name_month))[0]
    indexs=range((indexs[-1]+1),(T-1))
  for j in indexs:
        cons_dic[j]=df
# normalize #        
for t in range(0,T-1):
  cons=cons_dic[t]
  weight_s=cons['Weight']
  weight_na_s=weight_s.isna()
  na_count=sum(weight_na_s)
  if na_count>0:
    weight_s[weight_na_s]=(100-weight_s.dropna().sum())/na_count
  cons_dic[t]['Weight']=weight_s

# Data Preparation
  # EquityIndex Sector Constitutes Info
IndexSector=np.zeros(shape=(T,nsector))
for t in range(0,T-1):
    for i in range(0,nsector-1):
        cons=cons_dic[t]
        sector=SectorU[i]
        sector_s=SectorClass2.iloc[t,:]
        stock_codes=sector_s[sector_s==sector].index
        IndexSector[t,i]=cons[np.isin(cons.index,stock_codes)]['Weight'].sum()
IndexSector500=np.zeros(shape=(T,nsector))
for t in range(0,T-1):
  IndexSector500[t,]=IndexSector[t,]/IndexSector[t,].sum()


# Optimization Loop #
  # for loop for each trading day:
  	# 1. at time t determine which stocks to hold for t+1: index_jy 
index_jy=np.where(FV.iloc[t].rank(ascending=False)<=nsel)[0]

  	# 2. compute covariance matrix (corrected for zero diagonal term ) and sector-wise expected return
# H, SD & Alpha #
H=CC.iloc[(t-nmemory+1):(t+1),index_jy].cov()
h_diag=np.diag(H)
if np.any(h_diag==0):
  for s in np.where(h_diag==0)[0]:
      H[s,s]=np.mean(h_diag[h_diag!=0])
SD=np.diag(H)**0.5

if np.any(SD==0):
    for s in np.where(SD==0)[0]:
        SD[s]=np.mean(SD[SD!=0]) 
        
Alpha=np.zeros(nsel)
for i in range(0,nsector-1):
  index_jz=np.intersect1d(index_jy,np.where(SectorClass2.iloc[t-1,:]==SectorU[i])[0])
  lz=len(index_jz)
  index_js=np.where(np.isin(index_jy,index_jz))[0]
  ls=len(index_js)
  if (lz>1):
    Alpha[index_js]=CC.iloc[(t-nalpha+1):(t+1),index_jz].sum().sum()/np.sign(Volume.iloc[(t-nalpha+1):(t+1),index_jz]).sum().sum()

# cakk R package in python #
H=FRAPO.tdc(CC[(t-nmemory+1):(t+1),index_jy])
SD=self.CC.iloc[(t-self.nmemory+1):(t+1),index_jy].cov()**0.5

    # 3. run Portfolio Optimization: Constrained_OneStep_OptimFunc5.py and retrieve result for Wopt[t+1,index_jy]
op=self.Constrained_OneStep_OptimFunc5()
self.Wopt[t+1,index_jy]=op['w_opt']


# Optimization Main Function: Constrained_OneStep_OptimFunc5 #

# Constrained_OneStep_OptimFunc5.py
  # 1. Prepare for X_sector (sector constraint matrix) and X_style(Size and Beta constraint matrix) at each trading day
CodeX=cons_dic[t-1].index
index_jx=np.where(np.isin(Code,CodeX)==True)
index_jx=index_jx[0]
N=index_jx.size

X_sector=np.zeros(shape=(nsel,nsector))
for i in range(0,nsector-1):
  indexs=np.where(np.isin(SectorClass2.iloc[t-1,index_jy],SectorU[i]))[0]
  X_sector[indexs,i]=1

alpha_sector_up=np.zeros(shape=nsector)
alpha_sector_low=np.zeros(shape=nsector)
for i in range(0,nsector-1):
  alpha_sector_up[i]=IndexSector500[t-1,i]+sectorDeviation
  alpha_sector_low[i]=max(IndexSector500[t-1,i]-sectorDeviation,0)

wb=np.zeros(shape=N)
for i in range(0,N-1):
  index_js=np.where(np.isin(Code[index_jx],cons_dic[t-1].index))[0]
  wb[index_js]=cons_dic[t-1]['Weight']
wb=wb/sum(wb)

logsize=np.log(Size.iloc[t-1,index_jx])
if (np.any(np.isinf(logsize))): 
  logsize[np.isinf(logsize)]=logsize[~(np.isinf(logsize) | np.isnan(logsize))]

Index_Style=sum(logsize*wb)
alpha_style_up=np.zeros(shape=nstyle)
alpha_style_low=np.zeros(shape=nstyle)
X_style=np.zeros(shape=(nsel,nstyle))
# Size #
alpha_style_up[0]=Index_Style*1.05
alpha_style_low[0]=Index_Style*0.95
logsize2=np.log(Size.iloc[t-1,index_jy])
if (np.any(np.isinf(logsize2))): 
  logsize2[np.isinf(logsize2)]=logsize[~(np.isinf(logsize2) | np.isnan(logsize2))]
X_style[:,1]=logsize2

alpha_style_up[1]=1.2
alpha_style_low[1]=0.8
X_style[:,1]=Beta.iloc[t,index_jy]

  # 2. Run Optimization according to selected RiskMeasure
    # Risk_Adjusted_Return:    Constrained_MultiFactorModel_OptimFunc3()     
    # Risk_Parity:             Constrained_MultiFactorModel_OptimFunc5()           
    # Minimum_Tail_Dependent:  Constrained_MultiFactorModel_OptimFunc6()
    # Minimum_Variance:        Constrained_MultiFactorModel_OptimFunc3()
    # CVaR:                    Constrained_MultiFactorModel_OptimFunc7()

