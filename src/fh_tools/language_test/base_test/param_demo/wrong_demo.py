"""
@author  : MG
@Time    : 2020/12/17 15:02
@File    : wrong_demo.py
@contact : mmmaaaggg@163.com
@desc    : 用于
"""


def func(params=[1, 2, 3]):
    params.pop(0)
    print(params)


if __name__ == "__main__":
    func([4, 5, 6])
    func()
    func()
    func()
    func()
