#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2019/02/20 下午3:29
@File    : correlation_demo
@contact : mmmaaaggg@163.com
@desc    : correlation of pearsonr spearmanr
"""
import scipy.stats as stats

# pearsonr和spearmanr可以计算Pearson和Spearman相关系数，这两个相关系数度量了两组数据的相互线性关联程度：
norm_dist = stats.norm()
dat1 = norm_dist.rvs(size=100)
exp_dist = stats.expon()
dat2 = exp_dist.rvs(size=100)
cor, pval = stats.pearsonr(dat1, dat2)
print("Pearson correlation coefficient: " + str(cor))
cor, pval = stats.spearmanr(dat1, dat2)
print("Spearman's rank correlation coefficient: " + str(cor))
# Pearson correlation coefficient: -0.0345336831321
# Spearman's rank correlation coefficient: -0.0345336831321
# 其中的p-value表示原假设（两组数据不相关）下，相关系数的显著性。
