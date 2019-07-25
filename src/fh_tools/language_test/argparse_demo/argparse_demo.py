#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2019/7/9 21:18
@File    : argparse_demo.py
@contact : mmmaaaggg@163.com
@desc    : 
"""
import argparse


def main():
    parser = argparse.ArgumentParser(description="Demo of argparse")
    parser.add_argument('-n', '--name', default=' Li ')
    parser.add_argument('-y', '--year', default='20')
    parser.add_argument("-v", "--verbosity", action="store_true", help="increase output verbosity")
    # python argparse_demo.py --nargs2 a b
    parser.add_argument('--nargs2', nargs=2, default='d')
    # parser.add_argument('--nargs_', nargs='?', default='d')
    # parser.add_argument('--nargs__', nargs='+', default='d')
    args = parser.parse_args()
    print(args)
    print(f'Hello {args.name}  {args.year}')
    if args.verbosity:
        print("verbosity on")

    # args._get_kwargs()[('name', ' Li '), ('verbosity', False), ('year', '20')]
    print("args._get_kwargs()", args._get_kwargs())
    func(**dict(args._get_kwargs()))


def func(**kwargs):
    print('func(**kwargs) kwargs', kwargs)


if __name__ == '__main__':
    main()
