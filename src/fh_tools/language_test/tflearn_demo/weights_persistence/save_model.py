#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2019/5/3 10:57
@File    : save_model.py
@contact : mmmaaaggg@163.com
@desc    : 
"""
from __future__ import absolute_import, division, print_function

import tflearn

import tflearn.datasets.mnist as mnist

# MNIST Data
X, Y, testX, testY = mnist.load_data(one_hot=True)

# Model
input_layer = tflearn.input_data(shape=[None, 784], name='input')
dense1 = tflearn.fully_connected(input_layer, 128, name='dense1')
dense2 = tflearn.fully_connected(dense1, 256, name='dense2')
softmax = tflearn.fully_connected(dense2, 10, activation='softmax')
regression = tflearn.regression(softmax, optimizer='adam',
                                learning_rate=0.001,
                                loss='categorical_crossentropy')

# Define classifier, with model checkpoint (autosave)
model = tflearn.DNN(regression, checkpoint_path='model.tfl.ckpt')

# Train model, with model checkpoint every epoch and every 200 training steps.
model.fit(X, Y, n_epoch=1,
          validation_set=(testX, testY),
          show_metric=True,
          snapshot_epoch=True, # Snapshot (save & evaluate) model every epoch.
          snapshot_step=500, # Snapshot (save & evalaute) model every 500 steps.
          run_id='model_and_weights')


# ---------------------
# Save and load a model
# ---------------------

# Manually save model
model.save("model.tfl")
print('model saved on "model.tfl"')
