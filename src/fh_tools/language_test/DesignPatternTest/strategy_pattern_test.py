# -*- coding: utf-8 -*-
"""
参见流畅的python P281 策略模式
Created on 2017/9/29
@author: MG
"""

from abc import ABC, abstractmethod


class Promotion(ABC):  # 策略：抽象基类

    @abstractmethod
    def discount(self, order):
        """ 折扣"""

class FidelityPromo(Promotion): # 第一个具体策略
    """为积分为1000或以上的顾客提供5%折扣"""

    def discount(self, order):
        return order.total() * .05 if order.customer.fidelity >= 1000 else 0

class LargeOrderPromo(Promotion): # 第三个具体策略
    """订单中的不同商品达到10个或以上时提供7%折扣"""
    def discount(self, order):
        distinct_items = {item.product for item in order.cart}
        if len(distinct_items) >= 10:
            return order.total() * .07
        return 0

if __name__ == "__main__":
    fp = FidelityPromo()
    # 省略。。。。
