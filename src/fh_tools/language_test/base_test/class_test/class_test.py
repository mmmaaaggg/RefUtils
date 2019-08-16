# -*- coding: utf-8 -*-
"""
Created on 2017/6/12
@author: MG
"""


class A:
    def __init__(self):
        print('A')
        super().__init__()

    def func(self):
        print('A.func')


class B:
    def __init__(self):
        print('B')
        super().__init__()

    def func(self):
        print('B.func')

    def funcB(self):
        print('B.funcB')


class C(A, B):
    def __init__(self):
        # super(C, self).__init__()
        # A.__init__(self)
        # B.__init__(self)
        super().__init__()
        print('C')


obj = C()
# obj.func()
# obj.funcB()


# class B:
#     def __init__(self):
#         print("Enter B")
#         # print(super())
#         super().__init__()
#         print("Leave B")
#
#
# # single = B()
# # print(B.mro())
# class C:
#     def __init__(self):
#         print("Enter C")
#         # print(super())
#         super().__init__()
#         print("Leave C")
#
#
# class D(B, C):
#     def __init__(self):
#         print("Enter D")
#         # print(super())
#         super().__init__()
#         print("Leave D")
#
# D()