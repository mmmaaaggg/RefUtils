#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2019/02/20 下午3:20
@File    : describe_demo
@contact : mmmaaaggg@163.com
@desc    : stats.describe
"""
import scipy.stats as stats
norm_dist = stats.norm(loc=0, scale=1.8)
dat = norm_dist.rvs(size=100)
info = stats.describe(dat)
print("Data size is: " + str(info[0]))
print("Minimum value is: " + str(info[1][0]))
print("Maximum value is: " + str(info[1][1]))
print("Arithmetic mean is: " + str(info[2]))
print("Unbiased variance is: " + str(info[3]))
print("Biased skewness is: " + str(info[4]))
print("Biased kurtosis is: " + str(info[5]))

# Data size is: 100
# Minimum value is: -5.73556523159
# Maximum value is: 3.77439818033
# Arithmetic mean is: -0.00559348382755
# Unbiased variance is: 3.64113204268
# Biased skewness is: -0.600615731841
# Biased kurtosis is: 0.432147856587
