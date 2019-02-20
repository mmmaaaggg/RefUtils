#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2019/02/20 下午3:23
@File    : fit_demo
@contact : mmmaaaggg@163.com
@desc    :
"""
import scipy.stats as stats
# 当我们知道一组数据服从某些分布的时候，
# 可以调用fit函数来得到对应分布参数的极大似然估计（MLE, maximum-likelihood estimation）。
# 以下代码示例了假设数据服从正态分布，用极大似然估计分布参数：
norm_dist = stats.norm(loc=0, scale=1.8)
dat = norm_dist.rvs(size=100)
mu, sigma = stats.norm.fit(dat)
print("MLE of data mean:" + str(mu))
print("MLE of data standard deviation:" + str(sigma))

# MLE of data mean:0.00712958665203
# MLE of data standard deviation:1.71228079199
