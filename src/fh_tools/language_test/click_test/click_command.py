#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/9/28 8:47
@File    : click_command.py
@contact : mmmaaaggg@163.com
@desc    : 
"""
import click


def foo1():
    print('foo1')


def foo2():
    print('foo2')


func_list = [foo1, foo2]
promt_str = '   '.join(['%d) %s' % (num, foo.__name__) for num, foo in enumerate(func_list)])


@click.command()
@click.option('--foo', type=click.IntRange(0, len(func_list) - 1), prompt=promt_str)
@click.option('--init', type=click.BOOL, default=False)
def main(foo, init, **kwargs):
    if init:
        print('init')
    else:
        print(init)

    if foo is None:
        print("None")
    else:
        func_list[int(foo)]()


if __name__ == "__main__":
    main(standalone_mode=False)
