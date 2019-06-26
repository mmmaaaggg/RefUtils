# -*- coding: utf-8 -*-

import time
# import datetime
from datetime import datetime, timedelta
from calendar import monthrange


print('********time struct****************')
StrFormat_DateTime = "%Y.%m.%d %H:%M"
t = time.strptime('2012.01.30 1:59', StrFormat_DateTime)
timeStart = time.time()
print('time.time():', timeStart)
time.sleep(2)
timeEnd = time.time()
# print(timeEnd)
timeEstimate = timeEnd - timeStart
print('Estimate:%s' % timeEstimate)
timedelta(timeEstimate)
print('time.strptime: ', type(t), ' ', t)
print(time.strftime(StrFormat_DateTime, t))
print('***********datetime.datetime class***************')
dt = datetime.strptime('2016.01.03 1:59', StrFormat_DateTime).date()

print('datetime.datetime.strptime: ', type(dt), ' ', dt)
print("dt.strftime(StrFormat_DateTime)", dt.strftime(StrFormat_DateTime))
print("str(dt)", str(dt))

print('date 转换为 datetime')
dt = datetime(dt.year, dt.month, dt.day)
print(dt)

newtime = dt - timedelta(minutes=6)
print('current date:', newtime)
print('monthrange : ', monthrange(dt.year, dt.month))

weekday,daycount = monthrange(dt.year, dt.month)
daydelta = daycount - dt.day +1
nthday = dt.day % 7
newtime = dt + timedelta(days=daydelta)
print('next month:', newtime)

StrFormat_Date = "%Y-%m-%d"
DateStrList = [
    ['2015-9-1', '2015-9-15'],
    ['2015-10-1', '2015-10-15']]
DateList = [[i.strptime(StrFormat_Date) for i in n] for n in DateStrList]
print(DateList)

CheckDateStr = '2015-9-4'
CheckDate = datetime.strptime(CheckDateStr, StrFormat_Date)



print(DateList[0][0])
print(CheckDate)


def CheckDateInRange(DateList, CheckDate):
    for n in DateList:
        if n[0] < CheckDate and CheckDate < n[1]:
            return True
    return False

print(CheckDateInRange(DateList, CheckDate))


def counting_years(date_from_str, date_to_str):
    # date_from_str, date_to_str = '2018-05-01', '2019-05-31'
    date_from = datetime.strptime(date_from_str, '%Y-%m-%d')
    date_to = datetime.strptime(date_to_str, '%Y-%m-%d')

    year_start = datetime.strptime(f'{date_from.year}-01-01', '%Y-%m-%d')
    year_end = datetime.strptime(f'{date_from.year}-12-31', '%Y-%m-%d')
    ret_val1 = ((year_end - date_from).days + 1) / ((year_end - year_start).days + 1)

    year_start = datetime.strptime(f'{date_to.year}-01-01', '%Y-%m-%d')
    year_end = datetime.strptime(f'{date_to.year}-12-31', '%Y-%m-%d')
    ret_val2 = ((date_to - year_start).days + 1) / ((year_end - year_start).days + 1)

    ret_val = ret_val1 + ret_val2 + (date_to.year - date_from.year - 1)

    return ret_val
