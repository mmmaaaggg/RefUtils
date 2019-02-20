#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2019/02/20 下午3:39
@File    : linregress_demo
@contact : mmmaaaggg@163.com
@desc    : linregress
"""
import scipy.stats as stats
# 在分析金融数据中使用频繁的线性回归在SciPy中也有提供，我们来看一个例子：
x = stats.chi2.rvs(3, size=50)
y = 2.5 + 1.2 * x + stats.norm.rvs(size=50, loc=0, scale=1.5)
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
print("Slope of fitted model is:", slope)
print("Intercept of fitted model is:", intercept)
print("R-squared:", r_value**2)

# Slope of fitted model is: 1.20010505908
# Intercept of fitted model is: 2.04778311819
# R-squared: 0.781316678233
