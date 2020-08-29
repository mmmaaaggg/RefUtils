#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ver4,2017.12.21,pena added,robustcov available


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from cvxopt import matrix, solvers
import cvxopt as cvx
import sklearn.covariance as skc
from scipy.optimize import minimize


class PortConstructer():
    '''
    PortConstructer aims to construct portfolio by different methods
    
    df = pd.DataFrame(np.random.randn(10,3))  #收益矩阵
    pena = 0.1 #惩罚系数，惩罚偏离等权重的程度，增大时将会更加接近等权重，默认为0
    bnd = 0.8 #权重上限，默认为1
    PC = PortConstructer()
    PC.fitdf(df)  #df , DataFrame
    PC.fit(pena)
    PC.fit(bnd)
    PC.construct('EquWeight')  #or other methods,'InvVol',...
    mywgt = PC.wgt #Series, the best weight based on this method
    '''

    def __init__(self):
        self.pena = 0.0
        self.bnd = 1.0
        self.covtype = 'sample'
        pass

    def fitdf(self, df):
        self.df = df
        # self.wgt = pd.Series(0,index = df.columns)
        self.gchos = 1 - ((df == 0) | (np.isnan(df))).all()  # 删去空列及全零列，若全为0或者空则为0
        self.gchos = self.gchos[self.gchos == 1].index  ##数据正常的股票名
        self.gchos = df.iloc[-1, :].loc[self.gchos].dropna().index  # 删去当前不能交易列
        self.smalldf = df.loc[:, self.gchos].fillna(0)  ##可以交易的股票，补充0

    def fitpena(self, pena):
        self.pena = pena

    def fitbnd(self, bnd):
        self.bnd = bnd

    def covtype(self, covty):
        self.covtype = covty

    def showmethods(self):
        print('EqualWgt')
        print('InvVol')
        print('RiskPar')
        print('MinVar')
        print('MaxDiverse')
        print('MinTailDep')
        print('MinCVaR')

    def construct(self, method, cov_type='sample'):
        if not (method in ['EqualWgt', 'InvVol', 'RiskPar', 'MinVar', 'MaxDiverse', 'MinTailDep',
                           'MinCVaR']):
            print('unknown methods...')
            raise Warning

        if (method == 'EqualWgt'):
            wgt = pd.Series(1, index=self.smalldf.columns)
            wgt = wgt / np.nansum(wgt)
        if (method == 'InvVol'):
            wgt = self.smalldf.std() ** (-1)
            wgt[np.isinf(wgt)] = np.nan
            wgt = wgt / np.nansum(wgt)  # notice! NaN problem
        if (method == 'RiskPar'):
            wgt = riskparitywgtfind(robustcovest(self.smalldf, self.covtype) * 10000, self.bnd)  ##整体扩大协方差不会改变结果
        if (method == 'MinVar'):
            wgt = quad_form_opt(robustcovest(self.smalldf, self.covtype), self.pena, self.bnd)  ##需要自己改协方差的算法
        if (method == 'MaxDiverse'):
            wgt = quad_form_opt(self.smalldf.corr(), self.pena, self.bnd)
            wgt = wgt * self.smalldf.std() ** (-1)
            wgt[np.isinf(wgt)] = np.nan
            wgt = wgt / np.nansum(wgt)
        if (method == 'MinTailDep'):
            wgt = quad_form_opt(tail_dep(self.smalldf), self.pena, self.bnd)
            wgt = wgt * self.smalldf.std() ** (-1)
            # 容易出错！注意此处有inf会被nansum加入，从而分母是 inf
            wgt[np.isinf(wgt)] = np.nan
            wgt = wgt / np.nansum(wgt)
        if (method == 'MinCVaR'):
            [alpha, wgt] = cvar_opt(self.smalldf, 0.9)
            self.alpha = alpha

        self.wgt = pd.Series(0, index=self.df.columns)
        self.wgt.loc[self.gchos] = wgt.fillna(0)


def quad_form_opt(Q, pena=0.0, bnd=1.0):
    # new version 2017.12.23
    stklist = Q.index
    # Q = df.cov().fillna(0)  #Q should not contain NaN
    Q = np.matrix(Q)
    n = Q.shape[0]
    Q = Q + pena * np.eye(n)  # pena added
    solvers.options['show_progress'] = False
    Q = 2 * matrix(Q)
    q = matrix(0.0, (n, 1))
    G = np.vstack([np.eye(n), -np.eye(n)])
    G = matrix(G, (2 * n, n))
    h = matrix([bnd for i in range(n)] + [0.0 for i in range(n)], (2 * n, 1))
    A = matrix(1.0, (1, n))
    b = matrix(1.0)
    sol = solvers.qp(Q, q, G, h, A, b)
    return pd.Series(sol['x'], index=stklist)


def tail_dep(df):
    '''
    P = pd.DataFrame(0,index = df.columns,columns = df.columns)
    for i in range(P.shape[0]):
        for j in range(P.shape[1]):
            if (i>j):
                P.iloc[i,j] = P.iloc[j,i]
            else:
                P.iloc[i,j] = two_tail_dep(df.iloc[:,i],df.iloc[:,j])
    return P
    '''
    import rpy2.robjects as robjects
    from rpy2.robjects import pandas2ri
    pandas2ri.activate()
    robjects.r.source(r'E:\Dropbox\QT-Zeyu\Hantian\Code\taildep.r')
    res = robjects.r.tail_dep(pandas2ri.py2ri(df))
    return pd.DataFrame(np.matrix(res), index=df.columns, columns=df.columns)


def cvar_opt(ret, beta=0.9):
    q = ret.shape[0]
    n = ret.shape[1]
    c = 1 / (q * (1 - beta))
    p = [1] + [c for i in range(q)] + [0 for i in range(n)]
    p = matrix(p)
    G1 = np.eye(1 + q + n)
    G21 = np.ones(q).reshape(q, 1)
    G22 = np.eye(q)
    G2 = np.hstack([G21, G22, ret])
    G = matrix(-np.vstack([G1, G2]), (1 + n + 2 * q, 1 + n + q))  ##541,421
    h = matrix(0.0, (1 + 2 * q + n, 1))  ##541,1
    A = matrix([0.0 for i in range(1 + q)] + [1.0 for i in range(n)], (1, 1 + q + n))  ##1,421
    b = matrix(1.0, (1, 1))
    solvers.options['show_progress'] = False
    sol = solvers.lp(p, G, h, A, b)
    alpha = float(np.array(sol['x'])[0])
    x = np.array(sol['x'])[1 + q:].reshape(1, -1)[0]
    x = pd.Series(x, index=ret.columns)
    return [alpha, x]


def riskparitywgtfind(sigma, maxweight=1.0):
    def riskparity(x):
        n = len(sigma)
        w = np.mat(x).T
        port_var = np.sqrt(w.T * np.mat(sigma) * w)
        port_vec = np.mat(np.repeat(port_var / n, n)).T
        diag = np.mat(np.diag(x) / port_var)
        partial = np.mat(sigma) * w
        return np.square(port_vec - diag * partial).sum()

    cons = ({'type': 'eq', 'fun': lambda w: sum(w) - 1})
    bnds = ((0, maxweight),) * sigma.shape[0]
    w_ini = pd.Series([1 for i in range(sigma.shape[0])], index=sigma.index)
    w_ini = w_ini / sum(w_ini)
    res = minimize(riskparity, w_ini, bounds=bnds, constraints=cons, options={'disp': True, 'ftol': 10 ** -8},
                   method='SLSQP')
    return pd.Series(res['x'], index=sigma.index)


def robustcovest(df, covtype):
    if (covtype == 'sample'):
        return df.cov()
    if (covtype == 'LedoitWolf'):
        lw = skc.LedoitWolf()
        return pd.DataFrame(lw.fit(np.matrix(df)).covariance_, index=df.columns, columns=df.columns)
    if (covtype == 'MinDet'):
        return pd.DataFrame(skc.MinCovDet(assume_centered=True).fit(df).covariance_, index=df.columns,
                            columns=df.columns)
