#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2019/7/15 20:44
@File    : test_only.py
@contact : mmmaaaggg@163.com
@desc    : 
"""


class Package:
    def __init__(self, name, version, dependencies=[]):
        self.name = name
        self.version = version
        self.dependencies = dependencies


def calc_install_order(pkg_weighted_dic: dict, package_list: list, weight=1):
    """
    递归函数，用于计算所有需要安装的包
    :param pkg_weighted_dic: 安装包名称：（版本号，权重）
    :param package_list:
    :param weight:
    :return:
    """
    for pkg in package_list:
        if pkg.name in pkg_weighted_dic:
            version, weight_cur = pkg_weighted_dic[pkg.name]
            if weight > weight_cur:
                pkg_weighted_dic[pkg.name] = (version, weight)

        calc_install_order(pkg_weighted_dic, pkg.dependencies, weight + 1)


def main(package_list):
    """
    主函数
    :param package_list:需要安装的包列表
    :return:
    """
    pkg_weighted_dic = {}
    calc_install_order(pkg_weighted_dic, package_list, weight=1)
    pkg_install_ordered = [(name, _[0], _[1]) for name, _ in pkg_weighted_dic.items()]
    # 以 weight 为key进行倒排序
    pkg_install_ordered.sort(key=lambda x: x[2], reverse=True)

    return pkg_install_ordered


class Tree:
    def __init__(self):
        self.nodes = []
        self.value = None

    def traversal(self):
        print(self.value)
        for t in self.nodes:
            t.traversal()
