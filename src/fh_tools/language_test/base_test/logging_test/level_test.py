#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/9/26 15:56
@File    : level_test.py
@contact : mmmaaaggg@163.com
@desc    : 
"""
import logging

logger = logging.getLogger()


def parent_func():
    logger.info('log in parent function')
    son_func()


def son_func():
    logger.info('log in son function')
    logging.currentframe()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(filename)s.%(funcName)s:%(lineno)d|%(message)s')
    parent_func()
