# -*- coding: utf-8 -*-
"""
Created on 2017/4/5
@author: MG
相关语法参考：
https://www.cnblogs.com/huxi/archive/2010/07/04/1771073.html

"""
import re
"""
匹配如下字符串中含有股指的记录
3102
310205
31020512
310212
31021201
31021201IC1703
31021201IC1706
31021299
31021299IC1703
31021299IC1706
规则：
3102 + 四位数字 + IC1/IH1/IF1 + 三位数字
中间包含 IC1\IF1\IH1等字符
后面三个数字
"""
m = re.search(r"(?<=3102\d{4})(IC1|IF1|IH1)[0-9]{3}", '31021201IC1703')
if m is not None:
    print(m.group())
# 编译后运行效率更高
re_pattern = re.compile(r"(?<=3102\d{4})(IC1|IF1|IH1)[0-9]{3}")
m = re_pattern.search('31021201IC1703')
if m is not None:
    print(m.group())

m = re.search(r"(?<=【停牌】\()\d{4}-\d{1,2}-\d{1,2}", '【停牌】(2017-01-10)')
if m is not None:
    print(m.group())

#m = re.match(r"\d{6}99\d*", '11021199123')
m = re.match(r"\d{6}99\w*", '31021299IC1703')
if m is not None:
    print(m.group())

# 0.5人民币/千克
re_pattern = re.compile(r'\d*\.*\d*')
m = re_pattern.search(r"0.5人民币/千克")
if m is not None:
    print(m.group())

# AG1307.SHF
m = re.match(r"AG\d{4}\.SHF", 'AG1307.SHF')
if m is not None:
    print(m.group())

# 2017-12-15
# 2017/12/16
p = re.compile(r"\d{4}(.)\d{1,2}(.)\d{1,2}")
print(p.sub(r'%Y\1%m\2%d', '2017-12-15'))


# 估值表中股票相关科目
re_str = r"(?<=1102\d{2}[0-8]{2})\d{6}"
print("*"*20, re_str, "*"*20)
re_pattern_stock = re.compile(re_str)
str_list = ['110211', '11021101', '11021101603997', '11021199', '11021199600000', '11023101', '11023101000001']
for ss in str_list:
    m = re_pattern_stock.search(ss)
    if m is not None:
        print(m.group())

re_str = r'[A-Za-z]+(?=\d+$)'
print("*"*20, re_str, "*"*20)
re_pattern_instrument_header = re.compile(re_str)
str_list = ['rb1801', 'i1712', '1234', 'SPC a1801&m1709', 'SR807P6200']
for instrument_id in str_list:
    m = re_pattern_instrument_header.match(instrument_id)
    if m is None:
        print(instrument_id, '没有找到匹配的字符')
    else:
        print(instrument_id, '匹配', m.group())

re_str = r"\d{3,4}(?=.\w)"
print("*"*20, re_str, "*"*20)
re_pattern_instrument_header = re.compile(re_str)
str_list = ['AG9509.SHF', 'AG1209.SHF', 'I1109.DCE', 'AU9806.SHF']
for instrument_id in str_list:
    m = re_pattern_instrument_header.search(instrument_id)
    if m is None:
        print(instrument_id, '没有找到匹配的字符')
    else:
        print(instrument_id, '匹配', m.group())


def get_instrument_num(instrument_str):
    """
    获取合约的年月数字
    :param instrument_str: 
    :return: 
    """
    m = re_pattern_instrument_header.search(instrument_str)
    if m is None:
        raise ValueError('%s 不是有效的合约' % instrument_str)
    else:
        inst_num = int(m.group())
        inst_num = inst_num if inst_num < 9000 else inst_num - 10000
        return inst_num


str_list.sort(key=get_instrument_num)
print(str_list)

# 识别合约类型
re_str = r"[A-Za-z]+(?=\d{3,4}$)"
print("*"*20, re_str, "*"*20)
re_pattern_instrument_type = re.compile(re_str)
str_list = ['AG9509', 'AG1209', 'I1109', 'AU9806', "m1803-C-2400"]
for instrument_id in str_list:
    m = re_pattern_instrument_type.search(instrument_id)
    if m is None:
        print(instrument_id, '没有找到匹配的字符')
    else:
        print(instrument_id, '匹配', m.group())

wind_code_regexp = r'FHC-N\d{4}$'
m = re.match(wind_code_regexp, "FHC-N0000")
print(m)

re_str = r"(?<=(SR|CF))\d{3}(?=.CZC)"
print("*"*20, re_str, "*"*20)
re_pattern_instrument_type = re.compile(re_str)
str_list = ['SR0605.CZC', 'SR1605.CZC', 'SR607.CZC', 'cf806.CZC', "cf1803-C-2400"]
for instrument_id in str_list:
    m = re_pattern_instrument_type.search(instrument_id)
    if m is None:
        print(instrument_id, '没有找到匹配的字符')
    else:
        print(instrument_id, '匹配', m.group())

re_str = r"(?<=(SR|CF))\d{3}$"
print("*"*20, re_str, "*"*20)
re_pattern_instrument_type = re.compile(re_str)
str_list = ['SR0605', 'SR1605', 'SR607', 'cf806', 'RB1702', "cf1803-C-2400"]
for instrument_id in str_list:
    m = re_pattern_instrument_type.search(instrument_id)
    if m is None:
        print(instrument_id, '没有找到匹配的字符')
    else:
        print(instrument_id, '匹配', m.group())

re_str = r"\d{3,4}$"
print("*"*20, re_str, "*"*20)
re_pattern_instrument_type = re.compile(re_str)
str_list = ['SR0605', 'SR1605', 'SR607', 'cf806', 'RU9507', "cf1803-C-2400"]
for instrument_id in str_list:
    m = re_pattern_instrument_type.search(instrument_id)
    if m is None:
        print(instrument_id, '没有找到匹配的字符')
    else:
        print(instrument_id, '匹配', m.group())
