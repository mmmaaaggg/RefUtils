"""
@author  : MG
@Time    : 2021/3/10 7:40
@File    : foo_cls.py
@contact : mmmaaaggg@163.com
@desc    : 用于通过 side_effect 实现替换 class 实例方法函数为另一个指定函数
"""


class HelloFoo:
    def __init__(self, name):
        self.name = name

    def say(self, sth):
        print(f"{self.name}: {sth}")
        return f"{self.name}: {sth}"


if __name__ == "__main__":
    pass
