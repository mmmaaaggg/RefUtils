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
from src.fh_tools.fh_utils import date_2_str, str_2_date, try_2_date
from datetime import date, datetime
import logging
from src.nav_tools.read_nav_files import read_nav_files

logger = logging.getLogger()


def update_nav_file(file_path, fund_nav_dic, cash_df, nav_date=date.today()):
    """
    更新净值文件中的净值
    :param file_path:
    :param fund_nav_dic:
    :param cash_df:
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
        # 判断第一个cell是不是“基金名称”不是则跳过
        if sheet.cell_value(0, 0) != '基金名称':
            continue
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
        # 读取各种费用及借贷利息，子产品信息
        fee_dic, loan_dic = {}, {}
        row_num = 3
        cell_content = sheet.cell_value(row_num, 0)
        while cell_content != '日期' and cell_content != '':
            type_name = sheet.cell_value(row_num, 0)
            if type_name in ('费用', '费用（按子产品份额）'):
                # 费用
                name = sheet.cell_value(row_num, 0)
                fee_dic[name] = {
                    'name': sheet.cell_value(row_num, 0),
                    'rate': sheet.cell_value(row_num, 1),
                    'base_date': xlrd.xldate_as_datetime(sheet.cell_value(row_num, 3), 0).date(),
                }
                end_date = sheet.cell_value(row_num, 7)
                if end_date is not None and end_date != '':
                    # 有些管理费，分段计费
                    fee_dic[name]['end_date'] = xlrd.xldate_as_datetime(end_date, 0).date()

            elif type_name == '子产品':
                # 借款，子基金
                loan_dic[sheet.cell_value(row_num, 1)] = {
                    'name': sheet.cell_value(row_num, 1),
                    'rate': float(sheet.cell_value(row_num, 3)) if sheet.cell_value(row_num, 3) != '' else 0,
                    'base_date': xlrd.xldate_as_datetime(sheet.cell_value(row_num, 5), 0).date(),
                    'load_cost': float(sheet.cell_value(row_num, 7)) if sheet.cell_value(row_num, 7) != '' else 0,
                }
            else:
                logger.error('有未识别的行: %d 该行第一列值为：%s', row_num, type_name)

            row_num += 1
            cell_content = sheet.cell_value(row_num, 0)

        # 读取产品名称：横向读取每个产品名称间隔两个cell
        row_start, col_num = row_num, 1
        cell_content = sheet.cell_value(row_num, col_num)
        sub_product_name_list = []
        while cell_content != '':
            sub_product_name_list.append(cell_content)
            col_num += 3
            cell_content = sheet.cell_value(row_num, col_num)
        # 获取历史净值数据
        row_num = row_start + 1
        data_df = pd.read_excel(file_path, sheet_name=sheet_num, header=row_num, index_col=0).reset_index()
        data_df_new = data_df.append([None]).copy()
        last_row = data_df_new.shape[0] - 1
        data_df_new.iloc[last_row, 0] = nav_date
        tot_val = 0
        for prod_num, sub_product_name in enumerate(sub_product_name_list):
            col_num = 1 + prod_num * 3
            if sub_product_name in loan_dic:
                sub_product_info_dic = loan_dic[sub_product_name]
                rate = sub_product_info_dic['rate']
                if rate > 0:
                    nav, volume = 1, 0
                    # 借款：计算利息收入加上本金即为市值
                    # 市值
                    value = sub_product_info_dic['load_cost'] * (1 + sub_product_info_dic['rate']) * (
                            nav_date - sub_product_info_dic['base_date']).days / 365
                    data_df_new.iloc[last_row, col_num + 2] = value
                    tot_val += value
                else:
                    # 净值类产品
                    # nav = get_nav(product_name)
                    if sub_product_name in fund_nav_dic:
                        nav = fund_nav_dic[sub_product_name]
                    else:
                        logger.warning("%s 净值未查到，默认净值为 1", sub_product_name)
                        nav = 1

                    data_df_new.iloc[last_row, col_num] = nav
                    # 份额不变
                    volume = data_df_new.iloc[last_row - 1, col_num + 1]
                    data_df_new.iloc[last_row, col_num + 1] = volume
                    # 市值
                    value = float(data_df_new.iloc[last_row, col_num + 1]) * nav
                    data_df_new.iloc[last_row, col_num + 2] = value
                    tot_val += value
            else:
                nav = data_df_new.iloc[last_row - 1, col_num]
                volume = data_df_new.iloc[last_row - 1, col_num + 1]
                value = data_df_new.iloc[last_row - 1, col_num + 2]
                logger.error('子产品 %s 没有想过的基本信息，沿用上一计算日净值、份额、市值：',
                             sub_product_name, (nav, volume, value))
                data_df_new.iloc[last_row, col_num] = nav
                data_df_new.iloc[last_row, col_num + 1] = volume
                data_df_new.iloc[last_row, col_num + 2] = value

            # 保存子产品信息
            ret_data_dic['sub_product_list'].append({
                'product_name': sub_product_name,
                'volume': volume,
                'nav': nav,
                # 'nav_last': 1.1521,
                # 'nav_chg': 0.0025,
                # 'rr': 0.1325,
                # 'vol_pct': 0.1,  # 持仓比例
            })

        # 更新现金
        if cash_df is not None and fund_name in cash_df:
            pass
        else:
            logger.warning('没有找到 %d 现金余额， 使用上一次的数值', fund_name)
            cash = data_df_new['银行现金'].iloc[last_row - 1]
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
                worksheet.write(row_num, 1, value / 10000, style)
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
                            worksheet.write(row_real_num, 4, value / 10000, style)
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
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s: %(levelname)s [%(name)s] %(message)s')
    fund_nav_dic, cash_df = None, None
    # folder_path = r'd:\WSPych\RefUtils\src\fh_tools\nav_tools\product_nav'
    # folder_path_evaluation_table = r'D:\WSPycharm\fund_evaluation\evaluation_table'
    # folder_path_only_nav = r'D:\WSPycharm\fund_evaluation\only_nav'
    # folder_path_cash = r'D:\WSPycharm\fund_evaluation\cash'
    # folder_path_dict = {'folder_path_evaluation_table': folder_path_evaluation_table,
    #                     'folder_path_only_nav': folder_path_only_nav, 'folder_path_cash': folder_path_cash}
    # fund_nav_dic, cash_df = read_nav_files(folder_path_dict)
    file_path = r'd:\WSPych\RefUtils\src\nav_tools\净值计算模板 - 模测版.xls'
    ret_data_list = update_nav_file(file_path, fund_nav_dic, cash_df)
    # save_path = r'D:\WSPych\RefUtils\src\fh_tools\nav_tools\nav_summary.xls'
    # save_nav_files(ret_data_list, save_path)
