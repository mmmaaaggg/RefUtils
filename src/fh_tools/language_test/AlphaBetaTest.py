# -*- coding: utf-8 -*-

import numpy as np
from scipy.optimize import leastsq
from matplotlib import pyplot as plt
import math


def CalcAlphaBeta(indexA, indexB, x0=[0.01, 1], showplot=None):
    ''' 对任意两条相关曲线进行拟合，计算Alpha、Beta
    x0 为初始假设
    showplot 为可选参数 'raito' 'data' 'fit' 默认为None
    '''
    lenRange = np.array(list(range(len(indexA))))
    retb = (indexB - indexB[0]) / indexB[0]
    indexfit = (retb+1)*indexA[0]
    # print 'indexA'
    # print indexA
    # print 'indexfit'
    # print indexfit
    funcc = lambda x,p: indexA[x]*p[1] + x*p[0]
    residuals = lambda p, y, x: y - funcc(x, p)
    plsq = leastsq(residuals, x0, args=(indexfit, lenRange))
    if showplot == 'ratio':
        reta = (indexA - indexA[0]) / indexA[0]
        plt.plot(reta,'r')
        plt.plot(retb,'b')
        plt.legend(('A ratio', 'B ratio'), 'best', numpoints=1)# make legend
        plt.show()
    elif showplot == 'data':
        plt.plot(indexA,'r')
        plt.plot(indexfit,'b')
        plt.legend(('A data', 'B fit'), 'best', numpoints=1)# make legend
        plt.show()
    elif showplot == 'fit':
        plt.plot(indexA,'r')
        plt.plot(indexfit,'b')
        reta = (indexA - indexA[0]) / indexA[0]
        retfit = (reta+1)*plsq[0][1]*indexA[0] + lenRange*plsq[0][0]
        plt.plot(retfit,'g')
        plt.legend(('A data', 'B fit', 'ret fit'), 'best', numpoints=1)# make legend
        plt.show()
    return plsq


Beta =2
Alpha =0.02
lenx = 60
xlist = list(range(lenx)) #[float(n)/10*math.pi for n in ]
xarr = np.array(xlist)
indexy = np.sin(xarr.astype(float)/10*math.pi) + 10
CalcR = lambda arr: (arr-arr[0])/arr[0]
ra = CalcR(indexy)  # np.array([(indexy[n]-indexy[0])/indexy[n] for n in range(lenx-1)])
#stocky = indexy*A + xarr*k + np.random.randn(len(indexy))*0.3
startnum_index = 10
indexy = 20 * (ra+1)
stocky = 10 * (ra*Beta+1 + xarr * Alpha) + np.random.randn(lenx)*0.1

# plsq = leastsq(residuals, [1.5, 0.2], args=(stocky, xarr))
# plsq = CalcAlphaBeta(indexy, stocky, [1.5, 0.15])
plsq = CalcAlphaBeta(indexy, stocky)


print("真实[Alpha Beta]: [%f  %f]" % (Alpha, Beta)) 
print("拟合[Alpha Beta]:", plsq[0]) # 实验数据拟合后的参数

plt.plot(indexy)
plt.plot(stocky)

plt.show()
