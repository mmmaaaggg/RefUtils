#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 19-7-11 下午2:14
@File    : choice_demo.py
@contact : mmmaaaggg@163.com
@desc    : 
"""
import random

import numpy as np


def main(same_weight=True):
    ll, k = list(range(15)), 10
    if same_weight:
        result = random.choices(ll, k=10)
    else:
        weights = ll
        result = random.choices(ll, weights=weights, k=10)
    result.sort()

    print(f'有重复数据：random.choices:   list len={len(ll)} k={k}, same_weight={same_weight}\n\tresult3={result}')

    result2 = random.sample(ll, k=k)
    result2.sort()
    print(f'无重复数据：random.sample:    list len={len(ll)} k={k}\n\tresult3={result2}')

    if same_weight:
        result3 = np.random.choice(ll, k)
    else:
        result3 = np.random.choice(ll, k, p=np.array(ll) / sum(ll))
    result3.sort()
    print(f'有重复数据：np.random.choice: list len={len(ll)} k={k}, same_weight={same_weight}\n\tresult3={result3}')


def weighted_sample(ll, weights, k):
    """
    带权重、非重复取样
    :param ll:
    :param weights:
    :param k:
    :return:
    """
    ll_len = len(ll)
    if ll_len < k:
        raise ValueError(f"len(ll)={ll_len}<{k}")
    elif ll_len == k:
        return random.sample(ll, k)
    else:
        new_ll = list(range(len(ll)))
        new_ll_set = set(new_ll)
        new_weights = np.array(weights)
        new_k = k
        result_tot = []
        while True:
            result = random.choices(new_ll, weights=new_weights[new_ll], k=new_k)
            result_set = set(result)
            result_tot.extend(result_set)
            new_ll_set -= result_set
            new_k = k - len(result_tot)
            new_ll = list(new_ll_set)
            if new_k == 0:
                break

        result_tot.sort()
        if isinstance(ll, np.ndarray):
            ret = ll[result_tot]
        else:
            ret = [ll[_] for _ in result_tot]
        return ret


def _test_weighted_sample():
    ll = list(range(1, 30))
    result = weighted_sample(ll, weights=ll, k=15)
    print(result)
    ll = np.eye(29)
    result = weighted_sample(ll, weights=np.arange(1, 30), k=15)
    print(result)


if __name__ == "__main__":
    main(False)
    _test_weighted_sample()
