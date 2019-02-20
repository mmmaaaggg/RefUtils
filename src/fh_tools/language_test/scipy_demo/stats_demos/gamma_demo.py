#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2019/02/20 下午3:03
@File    : gamma_demo
@contact : mmmaaaggg@163.com
@desc    : demo scipy.stats.gamma
"""
import numpy as np
from scipy.stats import gamma
import scipy.stats as stats
import matplotlib.pyplot as plt


g_dist = stats.gamma(a=2)
print("quantiles of 2, 4 and 5:")
print(g_dist.cdf([2, 4, 5]))
print("Values of 25%, 50% and 90%:")
print(g_dist.pdf([0.25, 0.5, 0.95]))


fig, ax = plt.subplots(1, 1)

a = 1.99
mean, var, skew, kurt = gamma.stats(a, moments='mvsk')
# Display the probability density function (pdf):
x = np.linspace(gamma.ppf(0.01, a), gamma.ppf(0.99, a), 100)
ax.plot(x, gamma.pdf(x, a), 'r-', lw=5, alpha=0.6, label='gamma pdf 1.99')
ax.plot(x, gamma.pdf(x, 1.0), 'b-', lw=5, alpha=0.6, label='gamma pdf 1.00')
ax.plot(x, gamma.pdf(x, 3.0), 'g-', lw=5, alpha=0.6, label='gamma pdf 3.00')
ax.plot(x, gamma.pdf(x, 5.0), 'y-', lw=5, alpha=0.6, label='gamma pdf 5.00')
# Alternatively, the distribution object can be called (as a function)
# to fix the shape, location and scale parameters.
# This returns a “frozen” RV object holding the given parameters fixed.

# Freeze the distribution and display the frozen pdf:

rv = gamma(a)
ax.plot(x, rv.pdf(x), 'k-', lw=2, label='frozen pdf')
# Check accuracy of cdf and ppf:

vals = gamma.ppf([0.001, 0.5, 0.999], a)
np.allclose([0.001, 0.5, 0.999], gamma.cdf(vals, a))
# True
# Generate random numbers:

r = gamma.rvs(a, size=1000)
# And compare the histogram:

ax.hist(r, density=True, histtype='stepfilled', alpha=0.2)
ax.legend(loc='best', frameon=False)
plt.show(legend=True)
