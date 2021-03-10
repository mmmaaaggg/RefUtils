#! /usr/bin/env python3
"""
@author  : MG
@Time    : 2021/3/2 下午10:22
@File    : test_2.py
@contact : mmmaaaggg@163.com
@desc    : BALLOON
"""
from collections import Counter


def solution(S: str) -> int:
    counter = Counter(S)
    # BALLOON has 1 B, 1 A, 2 L, 2 O, 1 N
    consist = [
        ('B', 1),
        ('A', 1),
        ('L', 2),
        ('O', 2),
        ('N', 1), ]
    # count each letters times
    num_4_each_letter = [
        counter[letter] // count for letter, count in consist
    ]

    return min(num_4_each_letter)


if __name__ == "__main__":
    assert solution('BAONXXOLL') == 1
    assert solution('BAOOLLNNOLOLGBAX') == 2
