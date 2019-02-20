#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2019/02/20 下午3:28
@File    : moment_demo
@contact : mmmaaaggg@163.com
@desc    : moment
"""
import cripy.stats as stats

print(stats.norm.moment(6, loc=0, scale=1))
# 15.000000000895332
