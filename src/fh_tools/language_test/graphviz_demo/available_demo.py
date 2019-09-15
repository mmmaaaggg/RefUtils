#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2019/8/16 10:47
@File    : available_demo.py
@contact : mmmaaaggg@163.com
@desc    : 
"""

import os

os.environ["PATH"] += os.pathsep + 'C:\\IDE\\Graphviz2.38\\bin\\'
print('os.environ["PATH"]: \n', os.environ["PATH"])

from sklearn.datasets import load_iris
from sklearn import tree
import pydotplus

iris = load_iris()
clf = tree.DecisionTreeClassifier()
clf = clf.fit(iris.data, iris.target)

dot_data = tree.export_graphviz(clf, out_file=None,
                         feature_names=iris.feature_names,
                         class_names=iris.target_names,
                         filled=True, rounded=True,
                         special_characters=True)

graph = pydotplus.graph_from_dot_data(dot_data)
graph.write_pdf('iris.pdf')
