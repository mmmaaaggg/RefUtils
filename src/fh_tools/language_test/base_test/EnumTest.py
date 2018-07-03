from enum import IntEnum, unique


@unique
class PeriodType(IntEnum):
    """
    数字最小需要从1开始，顺序增长，每次+1，部分程序依赖于其最大数字以建立相应长度的list
    """
    Tick = 1
    Min1 = 2
    Min5 = 3
    Min15 = 4
    Hour1 = 5
    Day1 = 6
    Week1 = 7
    Mon1 = 8

# 不可修改
# PeriodType.Min1 = 2
MAX_PERIOD_TYPE_COUNT = int(max(PeriodType))
print(max(PeriodType), MAX_PERIOD_TYPE_COUNT)

# 类型转换
print("PeriodType(1)", PeriodType(1))  # <PeriodType.Tick: 1>
print("int(PeriodType.Min1)", int(PeriodType.Min1))
