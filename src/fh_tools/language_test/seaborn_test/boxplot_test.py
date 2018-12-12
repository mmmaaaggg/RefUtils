#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/12/11 15:23
@File    : seaborn_test.py
@contact : mmmaaaggg@163.com
@desc    : http://seaborn.pydata.org/generated/seaborn.boxplot.html
"""
import matplotlib.pyplot as plt
import seaborn as sns #要注意的是一旦导入了seaborn，matplotlib的默认作图风格就会被覆盖成seaborn的格式

sns.set(style="whitegrid")
tips = sns.load_dataset("tips")
# Draw a single horizontal boxplot:
ax = sns.boxplot(x=tips["total_bill"])
plt.show()

# Draw a vertical boxplot grouped by a categorical variable:
ax = sns.boxplot(x="day", y="total_bill", data=tips)
plt.savefig("vertical boxplot grouped by a categorical variable.jpg")
# plt.show()

# Draw a boxplot with nested grouping by two categorical variables:
ax = sns.boxplot(x="day", y="total_bill", hue="smoker", data=tips, palette="Set3")
plt.savefig("boxplot with nested grouping by two categorical variables.jpg")
# plt.show()

# Draw a boxplot with nested grouping when some bins are empty:
ax = sns.boxplot(x="day", y="total_bill", hue="time", data=tips, linewidth=2.5)
plt.savefig("boxplot with nested grouping when some bins are empty.jpg")
# plt.show()

# Control box order by passing an explicit order:
ax = sns.boxplot(x="time", y="tip", data=tips, order=["Dinner", "Lunch"])
plt.show()

# Use catplot() to combine a pointplot() and a FacetGrid. This allows grouping within additional categorical variables.
# Using catplot() is safer than using FacetGrid directly, as it ensures synchronization of variable order across facets:
g = sns.catplot(x="sex", y="total_bill", hue="smoker", col="time", data=tips, kind="box", height=4, aspect=.7)
plt.show()