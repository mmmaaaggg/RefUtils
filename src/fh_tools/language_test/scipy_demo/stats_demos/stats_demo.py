#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2019/02/20 上午10:43
@File    : stats_demo
@contact : mmmaaaggg@163.com
@desc    : 假设检验
"""
import scipy.stats as stats
import numpy as np

# 生成一组数据，并查看相关的统计量（相关分布的参数可以在
# https://docs.scipy.org/doc/scipy/reference/stats.html 查到）
norm_dist = stats.norm(loc=0.5, scale=2)
n = 200
dat = norm_dist.rvs(size=n)
print("mean of data is: " + str(np.mean(dat)))
print("median of data is: " + str(np.median(dat)))
print("standard deviation of data is: " + str(np.std(dat)))

# 假设这个数据是我们获取到的实际的某些数据，如股票日涨跌幅，我们对数据进行简单的分析。
# 最简单的是检验这一组数据是否服从假设的分布，如正态分布。
# 这个问题是典型的单样本假设检验问题，最为常见的解决方案是
# 采用K-S检验（ Kolmogorov-Smirnov test）。
# 单样本K-S检验的原假设是给定的数据来自和原假设分布相同的分布，在SciPy中提供了kstest函数，
# 参数分别是数据、拟检验的分布名称和对应的参数：

mu = np.mean(dat)
sigma = np.std(dat)
stat_val, p_val = stats.kstest(dat, 'norm', (mu, sigma))
print('KS-statistic D = %6.3f p-value = %6.4f (mu = %f, sigma= %f)' % (stat_val, p_val, mu, sigma))

# 假设检验的p-value值很大（在原假设下，p-value是服从[0, 1]区间上的均匀分布的随机变量，
# 可参考 http://en.wikipedia.org/wiki/P-value ），因此我们接受原假设，
# 即该数据通过了正态性的检验。在正态性的前提下，我们可进一步检验这组数据的均值是不是0。
# 典型的方法是t检验（t-test），其中单样本的t检验函数为ttest_1samp：

stat_val, p_val = stats.ttest_1samp(dat, 0)
print('One-sample t-statistic D = %6.3f, p-value = %6.4f' % (stat_val, p_val))

# 我们看到p-value<0.05，即给定显著性水平0.05的前提下，我们应拒绝原假设：
# 数据的均值为0。我们再生成一组数据，尝试一下双样本的t检验（ttest_ind）：

norm_dist2 = stats.norm(loc=-0.2, scale=1.2)
dat2 = norm_dist2.rvs(size=n/2)
stat_val, p_val = stats.ttest_ind(dat, dat2, equal_var=False)
print('Two-sample t-statistic D = %6.3f, p-value = %6.4f' % (stat_val, p_val))

# 注意，这里我们生成的第二组数据样本大小、方差和第一组均不相等，
# 在运用t检验时需要使用Welch's t-test，即指定ttest_ind中的equal_var=False。
# 我们同样得到了比较小的p-value$，在显著性水平0.05的前提下拒绝原假设，即认为两组数据均值不等。
# stats还提供其他大量的假设检验函数，如bartlett和levene用于检验方差是否相等；
# anderson_ksamp用于进行Anderson-Darling的K-样本检验等。
