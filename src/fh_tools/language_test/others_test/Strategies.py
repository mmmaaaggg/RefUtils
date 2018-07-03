# -*- coding:utf-8 -*-
import abc
import time
from enum import IntEnum, unique

from src.fh_tools.language_test import HandleData


@unique
class PeriodType(IntEnum):
    M1 = 1
    M5 = 2
    M15 = 3
    H1 = 4
    D1 = 5
    W1 = 6
    M1 = 7


class StrategyBase:
    '''策略类的父类，所有实现策略均需继承自该类实现他的相应函数'''

    def __init__(self, contractNo, periodType):
        '''初始化合约号、运行周期 '''
        self.context = dict()
        self.contractNo = contractNo
        self.periodType = periodType
        self.__positions = 0
        self.__balance = 0

        self.Initialize()

    filePath = '../Data/Gold1Min_2012.csv'

    @abc.abstractmethod
    def Initialize(self):
        # 依据合约号、运行周期 获取相应的初始化
        self.DataCount, self.CSVData = HandleData.LoadCSVData(StrategyBase.filePath)

    def RunInRange(self, datetimeFrmStr, datetimeToStr):
        # 输入策略运行时间范围，日期格式要符合 HandleData.StrFormat_DateTime
        datetimeFrm = time.strptime(datetimeFrmStr, HandleData.StrFormat_DateTime)
        datetimeTo = time.strptime(datetimeToStr, HandleData.StrFormat_DateTime)
        datetimeList = self.CSVData[0]
        kidFrm = datetimeList.index(datetimeFrm)
        kidTo = datetimeList.index(datetimeTo)
        self.Run(kidFrm, kidTo)

    def Run(self, kidFrm, kidTo):
        for nKid in range(kidFrm, kidTo - 1, -1):
            self.PrepareData(nKid)
            self.HandleData()
        self.Finalize()

    def PrepareData(self, nKid):
        # 对当前K先数据进行准备
        self.DateTime = self.CSVData[0][nKid:]
        self.Open = self.CSVData[1][nKid:]
        self.High = self.CSVData[2][nKid:]
        self.Low = self.CSVData[3][nKid:]
        self.Close = self.CSVData[4][nKid:]
        self.Vol = self.CSVData[5][nKid:]

    @abc.abstractmethod
    def HandleData(self):
        # 每一个 StrategyBase 的子类都重新此方法，实现具体策略运行逻辑
        pass

    @abc.abstractmethod
    def Finalize(self):
        pass

    def Sell(self, price, contractCount):
        self.HandleOrder(price, -contractCount)
        print('sell ' + self.contractNo + ' at ' + str(price) + ' on ' + time.strftime(HandleData.StrFormat_DateTime, self.DateTime[0]) + ' Position is ' + str(self.__positions))

    def Buy(self, price, contractCount):
        self.HandleOrder(price, contractCount)
        print('buy  ' + self.contractNo + ' at ' + str(price) + ' on ' + time.strftime(HandleData.StrFormat_DateTime, self.DateTime[0]) + ' Position is ' + str(self.__positions))

    def GetPositions(self):
        return self.__positions

    def GetBalance(self):
        return self.__balance

    def HandleOrder(self, price, contractCount):
        self.__balance = -price * contractCount
        self.__positions += contractCount


class EmptyStrategy(StrategyBase):

    @abc.abstractmethod
    def HandleData(self):
        ma5 = sum(self.Close[:5]) / 5
        close = self.Close[0]
        position = self.GetPositions()
        if close < ma5 and position >= 0:
            self.Sell(close, abs(-1 - position))
        elif close > ma5 and position <= 0:
            self.Buy(close, 1 - position)
        # print self.DateTime[0]
