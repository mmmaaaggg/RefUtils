#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2019/3/15 10:37
@File    : match.py
@contact : mmmaaaggg@163.com
@desc    : 针对阳君（苏玉洁）的朋友做的男女配对反向匹配的功能
"""
import pandas as pd


def get_best(df):
    # 互为对方第一选择的男、女编号（如有）
    print('\n1、互为对方第一选择的男、女编号（如有）')
    favor_dic = {}
    gender_dic = {}
    for i in range(df.shape[0]):
        code = df.iloc[i, 1]
        favor_code = set(df.iloc[i, 2:3])
        gender_dic[code] = df.iloc[i, 0]
        if '(空)' in favor_code:
            favor_code.remove('(空)')
        favor_dic[code] = favor_code

    matched_pair_list = []
    for num, (code, favor_code) in enumerate(favor_dic.items()):
        for code_pair in favor_code:
            if code_pair not in favor_dic:
                continue
            if code in favor_dic[code_pair]:
                matched_pair_list.append([gender_dic[code], code, gender_dic[code_pair], code_pair])
                print('%d) %s %d <-> %s %d' % (
                len(matched_pair_list), gender_dic[code], code, gender_dic[code_pair], code_pair))

    if len(matched_pair_list) == 0:
        print('没有结果')
    return matched_pair_list


def get_favor(df):
    # 互为对方选择的男、女编号
    print('\n2、互为对方选择的男、女编号')
    favor_dic = {}
    gender_dic = {}
    for i in range(df.shape[0]):
        code = df.iloc[i, 1]
        favor_code = set(df.iloc[i, 2:])
        gender_dic[code] = df.iloc[i, 0]
        if '(空)' in favor_code:
            favor_code.remove('(空)')
        favor_dic[code] = favor_code

    matched_pair_list = []
    for num, (code, favor_code) in enumerate(favor_dic.items()):
        for code_pair in favor_code:
            if code_pair not in favor_dic:
                continue
            if code in favor_dic[code_pair]:
                gender = gender_dic[code]
                # if gender == '男':
                #     matched_pair_list.append([code, gender, code_pair, gender_dic[code_pair]])
                # else:
                matched_pair_list.append([code_pair, gender_dic[code_pair], code, gender])
                # print(f'{len(matched_pair_list)}) {code}[{gender}] <-> {code_pair}[{gender_dic[code_pair]}]')

    if len(matched_pair_list) == 0:
        print('没有结果')
    match_df = pd.DataFrame(matched_pair_list, columns=['编号1', "性别1", "编号2", "性别2"])
    match_df.sort_values(['编号1', "编号2"], inplace=True)
    match_df.drop_duplicates(inplace=True)
    for num, (_, x) in enumerate(match_df.T.items(), start=1):
        print(f"{num}) {x['编号1']}[{x['性别1']}] <-> {x['编号2']}[{x['性别2']}]")
    return match_df


def get_chosen(df):
    # 每个人都被哪些人选择
    print('\n3、每个人都被哪些人选择：')
    chosen_dic = {}
    gender_dic = {}
    for i in range(df.shape[0]):
        code = df.iloc[i, 1]
        gender_dic[code] = df.iloc[i, 0]
        for favor_code in list(df.iloc[i, 2:]):
            if '(空)' == favor_code:
                continue
            if favor_code not in chosen_dic:
                chosen_dic[favor_code] = []

            chosen_dic[favor_code].append(code)

    for num, (chosen_code, code_list) in enumerate(chosen_dic.items()):
        gender = gender_dic[chosen_code] if chosen_code in gender_dic else ''
        # print("%d) %d[%s] 被 %d 人喜欢：%s" % (num, chosen_code, gender, len(code_list), code_list))

    df_chosen = pd.DataFrame([
        [chosen_code, gender_dic[chosen_code] if chosen_code in gender_dic else '', len(code_list)]
        for num, (chosen_code, code_list) in enumerate(chosen_dic.items())],
        columns=["编号", "性别", "被选择的次数"]
    )

    df_chosen.sort_values("编号", inplace=True)
    for num, (_, chosen_s) in enumerate(df_chosen.T.items(), start=1):
        chosen_code = chosen_s["编号"]
        code_list = chosen_dic[chosen_code]
        gender = gender_dic[chosen_code] if chosen_code in gender_dic else ''
        print("%d) %d[%s] 被 %d 人喜欢编号列表：%s" % (num, chosen_code, gender, len(code_list), code_list))

    return chosen_dic


def get_most_chosen(df):
    # 4、被异性选择最多的男、女编号
    print('\n4、被异性选择最多的男、女编号：')
    chosen_dic = {}
    gender_dic = {}
    for i in range(df.shape[0]):
        code = df.iloc[i, 1]
        gender_dic[code] = df.iloc[i, 0]
        for favor_code in list(df.iloc[i, 2:]):
            if '(空)' == favor_code:
                continue
            if favor_code not in chosen_dic:
                chosen_dic[favor_code] = []

            chosen_dic[favor_code].append(code)

    for num, (chosen_code, code_list) in enumerate(chosen_dic.items()):
        gender = gender_dic[chosen_code] if chosen_code in gender_dic else ''
        # print("%d) %d[%s] 被 %d 人喜欢：%s" % (num, chosen_code, gender, len(code_list), code_list))

    df_chosen = pd.DataFrame([
        [chosen_code, gender_dic[chosen_code] if chosen_code in gender_dic else '', len(code_list)]
        for num, (chosen_code, code_list) in enumerate(chosen_dic.items())],
        columns=["编号", "性别", "被选择的次数"]
    )
    df_chosen.sort_values("被选择的次数", ascending=False, inplace=True)
    boy_favorate = df_chosen[df_chosen["性别"] == '男'].iloc[0, :]
    girl_favorate = df_chosen[df_chosen["性别"] == '女'].iloc[0, :]
    print('最受欢迎的男士，编号 %d 被 %d 人喜欢' % (boy_favorate["编号"], boy_favorate["被选择的次数"]))
    print('最受欢迎的女士，编号 %d 被 %d 人喜欢' % (girl_favorate["编号"], girl_favorate["被选择的次数"]))
    # print(df_chosen)
    return df_chosen


if __name__ == "__main__":
    df = pd.read_excel(r'C:\GitHub\RefUtils\src\fh_tools\language_test\xlrd_demo\match_girl_boy\提交结果_final.xlsx')
    best_match = get_best(df)
    favor_match = get_favor(df)
    favor_match.to_excel(r'C:\GitHub\RefUtils\src\fh_tools\language_test\xlrd_demo\match_girl_boy\favor_match.xls', index=False)
    chosen_dic = get_chosen(df)
    df_chosen = get_most_chosen(df)
    df_chosen.to_excel(r'C:\GitHub\RefUtils\src\fh_tools\language_test\xlrd_demo\match_girl_boy\favor_chosen.xls', index=False)
