# -*- coding:utf-8 -*-
import csv
import time

StrFormat_DateTime = "%Y.%m.%d %H:%M"

InsertIndex = 0


def LoadCSVData(fileName):
    f = open(fileName, 'r')
    reader = csv.reader(f)
    datetimeList, openList, highList, lowList, closeList, volList = [], [], [], [], [], []
    for dateStr, timeStr, openStr, highStr, lowStr, closeStr, volStr in reader:
        # 2012.01.03 1:51 1570.25 1570.25 1570.19 1570.19
        # print dateStr, timeStr, openStr, highStr, lowStr, closeStr
        if timeStr == '4:00':
            break
        datetimeStr = ' '.join([dateStr, timeStr])
        datetimeList.insert(InsertIndex, time.strptime(datetimeStr, StrFormat_DateTime))
        openList.insert(InsertIndex, float(openStr))
        highList.insert(InsertIndex, float(highStr))
        lowList.insert(InsertIndex, float(lowStr))
        closeList.insert(InsertIndex, float(closeStr))
        volList.insert(InsertIndex, float(volStr))
    CSVData = [datetimeList, openList, highList, lowList, closeList, volList]
    return len(datetimeList), CSVData

#DataCount, CSVData = LoadCSVData('../Data/Gold1Min_2012.csv')
# print DataCount
