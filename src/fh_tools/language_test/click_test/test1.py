#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/9/28 9:04
@File    : test1.py
@contact : mmmaaaggg@163.com
@desc    : 
"""

import click

@click.command()
@click.option('--rate', type=float, help='rate')   # 指定 rate 是 float 类型
def show(rate):
    click.echo('rate: %s' % rate)

if __name__ == '__main__':
    show()
