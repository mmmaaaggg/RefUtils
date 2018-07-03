#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/4/25 17:45
@File    : adboost_test.py
@contact : mmmaaaggg@163.com
@desc    : 
"""
from sklearn import linear_model, decomposition, ensemble, preprocessing, isotonic, metrics
import pandas as pd


x_train_data = [
    [1, 2, 3],
    [2, 3, 4],
    [4, 5, 6],
    [2, 1, 0],
    [3, 2, 1],
]
y_train_data = [1, 1, 1, 0, 0]
x_test_data = [
    [10, 11, 12],
    [15, 21, 25],
    [21, 32, 43],
    [3, 1, 0],
    [2, 1, 0],
]

x_train_df = pd.DataFrame(x_train_data, columns=['a', 'b', 'c'])
# y_train_df = pd.DataFrame(y_train_data, columns=['y'])
y_train_df = pd.Series(y_train_data, name='y')

# 用AdaBoost训练
# Train classifier
scaler = preprocessing.MinMaxScaler()
clf = ensemble.AdaBoostClassifier(n_estimators=150)  # n_estimators controls how many weak classifiers are fi

x_train_fit_df = scaler.fit_transform(x_train_df)
clf.fit(x_train_fit_df, y_train_df)

# 看看训练结果
x_test_df = pd.DataFrame(x_test_data, columns=['a', 'b', 'c'])
y_test_pred = clf.predict(x_test_df)
y_test_pred_prob = clf.predict_proba(x_test_df)
print("y_test_pred:\n", y_test_pred)
print("y_test_pred_prob:\n", y_test_pred_prob)
