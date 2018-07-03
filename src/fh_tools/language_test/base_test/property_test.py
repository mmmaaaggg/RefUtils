# -*- coding: utf-8 -*-
"""
Created on 2017/6/20
@author: MG
"""


class Person:

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        self.full_name = [first_name, last_name]

    @property
    def full_name(self):
        return " ".join([self.first_name, self.last_name])

    @full_name.setter
    def full_name(self, full_name):
        print('set full name:', full_name)
        self.first_name = full_name[0]
        self.last_name = full_name[1]


class StrategyOrder:
    """
    用户记录用户从 ReqOrderInsert, OnRspOrderInsert, 只到 OnRtnTrade 的全部数据信息
    """

    def __init__(self, strategy_id, input_order):
        """
        用户记录用户从 ReqOrderInsert 请求中的 strategy_id, input_order
        :param strategy_id: 
        :param input_order: 
        """
        self.__strategy_id = strategy_id
        self.__input_order = None
        self.__trade = None
        self.input_order = input_order

    @property
    def strategy_id(self):
        return self.__strategy_id

    @property
    def input_order(self):
        return self.__input_order

    @input_order.setter
    def input_order(self, input_order):
        self.__input_order = input_order
        # with with_mongo_client() as client:
        #     db = client[Config.MONGO_DB_NAME]
        #     collection = db[Config.MONGO_COLLECTION_INPUT_ORDER]
        #     collection.insert_one(input_order)


    @property
    def trade(self):
        return self.__trade

    @trade.setter
    def set_trade(self, trade):
        self.__trade = trade

if __name__ == '__main__':
    p = Person('fname', 'lname')
    print('full_name:', p.full_name)
    p.full_name = ('asdf', 'ffff')
    print(p.full_name)
