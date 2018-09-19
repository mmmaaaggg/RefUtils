#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/9/17 9:57
@File    : calc_nav.py
@contact : mmmaaaggg@163.com
@desc    : openpyxl, pandas, xlrd
"""
import xlrd
import xlutils.copy
import xlwt
import re
import os
import pandas as pd
from src.fh_tools.fh_utils import date_2_str, str_2_date
from datetime import date, datetime
import logging

logger = logging.getLogger()


def update_nav_file(file_path, fund_nav_dic, cash_dic=None, nav_date=date.today()):
    """
    更新净值文件中的净值
    :param file_path:
    :param fund_nav_dic:
    :param cash_dic:
    :param nav_date:
    :return:
    """
    # nav_date 日期转换
    if nav_date is None:
        nav_date = date.today()
    elif isinstance(nav_date, str):
        nav_date = str_2_date(nav_date)

    ret_data_list = []
    file_path_name, file_extension = os.path.splitext(file_path)

    workbook = xlrd.open_workbook(file_path)
    sheet_names = workbook.sheet_names()
    for sheet_num, sheet_name in enumerate(sheet_names, start=0):
        sheet = workbook.sheet_by_name(sheet_name)
        # 取得名称，日期，份额数据
        fund_name = sheet.cell_value(0, 1)
        setup_date = xlrd.xldate_as_datetime(sheet.cell_value(1, 1), 0).date()
        fund_volume = sheet.cell_value(2, 1)
        ret_data_dic = {
            'product_name': fund_name,
            'setup_date': setup_date,
            'volume': fund_volume,
            'sub_product_list': [],
        }
        # 读取各种费用及借贷利息等信息
        fee_dic, loan_dic, name_last = {}, {}, ''
        row_num = 3
        cell_content = sheet.cell_value(row_num, 0)
        while cell_content != '日期' and cell_content != '':
            load_cost = sheet.cell_value(row_num, 5)
            if load_cost == '':
                # 费用
                name = sheet.cell_value(row_num, 0)
                fee_dic[name] = {
                    'name': sheet.cell_value(row_num, 0),
                    'rate': sheet.cell_value(row_num, 1),
                    'base_date': xlrd.xldate_as_datetime(sheet.cell_value(row_num, 3), 0).date(),
                }
                if name_last.find('管理费') == 0:
                    # 有些管理费，分段计费
                    fee_dic[name_last]['end_date'] = xlrd.xldate_as_datetime(sheet.cell_value(row_num, 3), 0).date()
            else:
                # 借款
                loan_dic[sheet.cell_value(row_num, 0)] = {
                    'name': sheet.cell_value(row_num, 0),
                    'rate': sheet.cell_value(row_num, 1),
                    'base_date': xlrd.xldate_as_datetime(sheet.cell_value(row_num, 3), 0).date(),
                    'load_cost': sheet.cell_value(row_num, 3),
                }
            row_num += 1
            cell_content = sheet.cell_value(row_num, 0)

        # 读取产品名称
        col_num = 1
        cell_content = sheet.cell_value(row_num, col_num)
        product_name_list = []
        while cell_content != '':
            product_name_list.append(cell_content)
            col_num += 3
            cell_content = sheet.cell_value(row_num, col_num)
        # 获取历史净值数据
        row_num += 1
        data_df = pd.read_excel(file_path, sheet_name=sheet_num, header=row_num, index_col=0).reset_index()
        data_df_new = data_df.append([None]).copy()
        last_row = data_df_new.shape[0] - 1
        data_df_new.iloc[last_row, 0] = nav_date
        tot_val = 0
        for prod_num, product_name in enumerate(product_name_list):
            col_num = 1 + prod_num * 3
            if product_name in loan_dic:
                nav, volume = 1, 0
                # 借款：计算利息收入加上本金即为市值
                # 市值
                load_info_dic = loan_dic[product_name]
                value = load_info_dic['load_cost'] * (1 + load_info_dic['rate']) * (
                        nav_date - load_info_dic['base_date']).days / 365
                data_df_new.iloc[last_row, col_num + 2] = value
                tot_val += value
            else:
                # 净值类产品
                # nav = get_nav(product_name)
                if product_name in fund_nav_dic:
                    nav = fund_nav_dic[product_name]
                else:
                    logger.warning("%s 净值未查到，默认净值为 1", product_name)
                    nav = 1

                data_df_new.iloc[last_row, col_num] = nav
                # 份额不变
                volume = data_df_new.iloc[last_row - 1, col_num + 1]
                data_df_new.iloc[last_row, col_num + 1] = volume
                # 市值
                value = float(data_df_new.iloc[last_row, col_num + 1]) * nav
                data_df_new.iloc[last_row, col_num + 2] = value
                tot_val += value

            # 保存子产品信息
            ret_data_dic['sub_product_list'].append({
                'product_name': product_name,
                'volume': volume,
                'nav': nav,
                # 'nav_last': 1.1521,
                # 'nav_chg': 0.0025,
                # 'rr': 0.1325,
                # 'vol_pct': 0.1,  # 持仓比例
            })

        # 更新现金
        if cash_dic is None:
            cash = data_df_new['银行现金'].iloc[last_row - 1]
        else:
            cash = 0
        data_df_new['银行现金'].iloc[last_row] = cash
        tot_val += cash

        # 计算费用
        tot_fee = 0
        for key, info_dic in fee_dic.items():
            end_date = info_dic.setdefault('end_date', nav_date)
            manage_fee = - (end_date - info_dic['base_date']).days / 365 * fund_volume * info_dic['rate']
            data_df_new[key].iloc[last_row] = manage_fee
            tot_fee += manage_fee

        # 计算新净值
        data_df_new['总市值（费前）'].iloc[last_row] = tot_val
        data_df_new['总市值（费后）'].iloc[last_row] = tot_val + tot_fee
        data_df_new['净值（费前）'].iloc[last_row] = tot_val / fund_volume
        data_df_new['净值（费后）'].iloc[last_row] = nav = (tot_val + tot_fee) / fund_volume

        # 保存文件
        # 再源文件基础上增量更新
        file_path_new = file_path_name + '_' + date_2_str(nav_date) + file_extension
        workbook_new = xlutils.copy.copy(workbook)
        sheet = workbook_new.get_sheet(sheet_num)
        # nav_date
        style = xlwt.XFStyle()
        style.num_format_str = 'YYYY/M/D'
        sheet.write(row_num + last_row + 1, 0, nav_date, style)
        # 各个产品的【净值	份额	市值】
        # 银行现金	管理费1	管理费2	托管费	总市值（费前）	净值（费前）	总市值（费后）	净值（费后）
        col_len = data_df_new.shape[1]
        for col_num in range(1, col_len):
            value = data_df_new.iloc[last_row, col_num]
            if value is None:
                continue
            style = xlwt.XFStyle()
            style.num_format_str = '_(#,##0.00_);[Red](#,##0.00)'
            sheet.write(row_num + last_row + 1, col_num, value, style)
        workbook_new.save(file_path_new)
        # 保存独立 DataFrame 文件
        file_path_df = file_path_name + '_df_' + date_2_str(nav_date) + file_extension
        data_df_new.to_excel(file_path_df)
        # 保存返回信息
        ret_data_dic['nav'] = nav
        nav_last = data_df_new['净值（费后）'].iloc[last_row - 1]
        ret_data_dic['nav_last'] = nav_last
        ret_data_dic['nav_chg'] = nav - nav_last
        ret_data_dic['rr'] = nav ** (365 / (nav_date - setup_date).days) if (nav_date - setup_date).days > 10 else 0.0
        ret_data_list.append(ret_data_dic)

    return ret_data_list


def read_nav_files(folder_path):
    fund_dictionay = {}
    # folder_path = r'D:\WSPycharm\fund_evaluation\contact'
    file_names = os.listdir(folder_path)
    for file_name in file_names:
        # file_path = r'd:\Works\F复华投资\合同、协议\丰润\丰润一期\SK8992_复华丰润稳健一期_估值表_20170113.xls'
        file_path = os.path.join(folder_path, file_name)
        file_name_net, file_extension = os.path.splitext(file_path)
        if file_extension not in ('.xls', '.xlsx'):
            continue
        else:
            data_df = pd.read_excel(file_path, skiprows=1, header=0)
            # 获取净值
            data_df1 = pd.read_excel(file_path, skiprows=3, header=0)
            cum_nav = data_df1['科目名称'][data_df1['科目代码'] == '累计单位净值:']
            name, nav = data_df.columns[0][13:-6], float(cum_nav.values[0])
            fund_dictionay[name] = nav

    return fund_dictionay


def save_nav_files(data_list, save_path):
    # 创建excel工作表
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('sheet1')
    # 设置表头
    worksheet.write(0, 0, label='产品名称')  # product_name
    worksheet.write(0, 1, label='产品规模（万）')  # volume
    worksheet.write(0, 2, label='基金成立日期')  # setup_date
    worksheet.write(0, 3, label='所投资管计划/信托计划名称')  # sub_product_list
    worksheet.write(0, 4, label='子基金所投规模（万）')  # volume
    worksheet.write(0, 5, label='子基金净值')  # nav
    worksheet.write(0, 6, label='子基金上期净值')  # nav_last
    worksheet.write(0, 7, label='子基金净值变动率')  # nav_chg
    worksheet.write(0, 8, label='子基金收益率（年化）')  # rr
    worksheet.write(0, 9, label='子基金持仓比例')  # vol_pct
    worksheet.write(0, 10, label='基金净值')  # nav
    worksheet.write(0, 11, label='上期净值')  # nav_last
    worksheet.write(0, 12, label='收益率（年化）')  # rr
    worksheet.write(0, 13, label='净值变动率')  # nav_chg
    # 将数据写入excel
    row_num = 0
    for list_item in data_list:
        row_num += 1
        row_sub_num = -1
        for key, value in list_item.items():
            if key == "product_name":
                worksheet.write(row_num, 0, value)
            elif key == "volume":
                style = xlwt.XFStyle()
                style.num_format_str = '_(#,##0_);(#,##0)'
                worksheet.write(row_num, 1, value/10000, style)
            elif key == "setup_date":
                style = xlwt.XFStyle()
                style.num_format_str = 'YYYY/M/D'
                worksheet.write(row_num, 2, value, style)
            elif key == "nav":
                style = xlwt.XFStyle()
                style.num_format_str = '0.00'
                worksheet.write(row_num, 10, value, style)
            elif key == "nav_last":
                style = xlwt.XFStyle()
                style.num_format_str = '0.00'
                worksheet.write(row_num, 11, value, style)
            elif key == "rr":
                style = xlwt.XFStyle()
                style.num_format_str = '0.00%'
                worksheet.write(row_num, 12, value, style)
            elif key == "nav_chg":
                style = xlwt.XFStyle()
                style.num_format_str = '_(#,##0.00_);[Red](#,##0.00)'
                value = - value
                worksheet.write(row_num, 13, value, style)
            elif key == "sub_product_list":
                for list_item_sub in data_list[0]['sub_product_list']:
                    row_sub_num += 1
                    for key, value in list_item_sub.items():
                        row_real_num = row_num + row_sub_num
                        if key == "product_name":
                            worksheet.write(row_real_num, 3, value)
                        elif key == "volume":
                            style = xlwt.XFStyle()
                            style.num_format_str = '_(#,##0_);(#,##0)'
                            worksheet.write(row_real_num, 4, value/10000, style)
                        elif key == "nav":
                            style = xlwt.XFStyle()
                            style.num_format_str = '0.00'
                            worksheet.write(row_real_num, 5, value, style)
                        elif key == "nav_last":
                            style = xlwt.XFStyle()
                            style.num_format_str = '0.00'
                            worksheet.write(row_real_num, 6, value, style)
                        elif key == "nav_chg":
                            style = xlwt.XFStyle()
                            style.num_format_str = '_(#,##0.00_);[Red](#,##0.00)'
                            worksheet.write(row_real_num, 7, value, style)
                        elif key == "rr":
                            style = xlwt.XFStyle()
                            style.num_format_str = '0.00%'
                            worksheet.write(row_real_num, 8, value, style)
                        elif key == "vol_pct":
                            style = xlwt.XFStyle()
                            style.num_format_str = '0.00%'
                            worksheet.write(row_real_num, 9, value, style)
            else:
                pass
        if row_sub_num >= 0:
            row_num += row_sub_num
    # 保存
    workbook.save(save_path)


if __name__ == "__main__":
    folder_path = r'd:\WSPych\RefUtils\src\fh_tools\nav_tools\product_nav'
    fund_nav_dic = read_nav_files(folder_path)
    file_path = r'D:\WSPych\RefUtils\src\fh_tools\nav_tools\净值计算模板 - 完整版.xls'
    ret_data_list = update_nav_file(file_path, fund_nav_dic, cash_dic=None)
    save_path = r'D:\WSPych\RefUtils\src\fh_tools\nav_tools\nav_summary.xls'
    save_nav_files(ret_data_list, save_path)
    # print(ret_data_list)
    # data_list = [
    #     {
    #         'product_name': '复华财通定增投资基金',
    #         'volume': 3924.53,
    #         'setup_date': str_2_date('2013-12-31'),
    #         'nav': 1.1492,
    #         'nav_last': 1.1521,
    #         'nav_chg': 0.0025,
    #         'rr': 0.1325,
    #         'sub_product_list': [
    #             {
    #                 'product_name': '展弘稳进1号',
    #                 'volume': 400.00,
    #                 'nav': 1.1492,
    #                 'nav_last': 1.1521,
    #                 'nav_chg': 0.0025,
    #                 'rr': 0.1325,
    #                 'vol_pct': 0.1,  # 持仓比例
    #             },
    #             {
    #                 'product_name': '新萌亮点1号',
    #                 'volume': 800.00,
    #                 'nav': 1.1592,
    #                 'nav_last': 1.1721,
    #                 'nav_chg': 0.0025,
    #                 'rr': 0.1425,
    #                 'vol_pct': 0.2,  # 持仓比例
    #             },
    #         ],
    #     },
    #     {
    #         'product_name': '鑫隆稳进FOF',
    #         'volume': 3924.53,
    #         'setup_date': str_2_date('2013-12-31'),
    #         'sub_product_list': [
    #             {
    #                 'product_name': '展弘稳进1号',
    #                 'volume': 400.00,
    #                 'nav': 1.1492,
    #                 'nav_last': 1.1521,
    #                 'nav_chg': 0.0025,
    #                 'rr': 0.1325,
    #                 'vol_pct': 0.1,  # 持仓比例
    #             },
    #             {
    #                 'product_name': '新萌亮点1号',
    #                 'volume': 800.00,
    #                 'nav': 1.1592,
    #                 'nav_last': 1.1721,
    #                 'nav_chg': 0.0025,
    #                 'rr': 0.1425,
    #                 'vol_pct': 0.2,  # 持仓比例
    #             },
    #         ],
    #         'nav': 1.1492,
    #         'nav_last': 1.1521,
    #         'nav_chg': 0.0025,
    #         'rr': 0.1325,
    #     },
    # ]
