#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/8/1 8:31
@File    : only_test.py
@contact : mmmaaaggg@163.com
@desc    : 
"""
import psutil
import win32api
import win32con
from ctypes import windll
import win32gui
import pywintypes
import time
import requests
import pandas as pd
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import logging
import subprocess


logger = logging.getLogger()
# ------------------ 以下代码均出自其他模块点，主要为了自然关闭 shadow socks--------------------------


def mouse_move(x, y):
    windll.user32.SetCursorPos(x, y)


def mouse_click(x=None, y=None, button='left'):
    if x is not None and y is not None:
        mouse_move(x, y)
        time.sleep(0.05)
    if button == 'left':
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    elif button == 'right':
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
    else:
        raise ValueError('button=%s 不支持' % button)


def find_hwnds_by_matchers(matcher_list, hwnd_parent=None):
    """
    通过子控件标题栏内容找到对应控件
    :param matcher_list: tuple 列表 第一项为 'windows' 'DlgItem' 第二项为 相关参数或 lambda 列表
    :param hwnd_parent: 母窗口（控件）ID
    :return: 返回ID列表，如果 macher_list中有任一项无法匹配，则返回 None
    """
    hwnd_list_ret = []
    matcher_count = len(matcher_list)
    if matcher_count == 0:
        return None
    matcher_type = matcher_list[0][0]
    # 如果 matcher_type 是 window，则为 lambda 表达式
    # 如果 matcher_type 是 DlgItem，则为 item_id
    item_id = func = matcher_list[0][1]
    exp_count = 0
    hwnd = None
    if matcher_type == 'window':
        while hwnd is None or hwnd != 0:
            hwnd = win32gui.FindWindowEx(hwnd_parent, hwnd, None, None)
            if hwnd == 0:
                break
            is_ok = func(hwnd)
            if is_ok:
                if matcher_count > 1:
                    hwnd_list = find_hwnds_by_matchers(matcher_list[1:], hwnd_parent=hwnd)
                    if hwnd_list is None or len(hwnd_list) == 0:
                        continue
                    hwnd_list_ret.append(hwnd)
                    hwnd_list_ret.extend(hwnd_list)
                else:
                    hwnd_list_ret.append(hwnd)
                return hwnd_list_ret
    elif matcher_type == 'DlgItem':
        try:
            hwnd = win32gui.GetDlgItem(hwnd_parent, item_id)
            if matcher_count > 1:
                hwnd_list = find_hwnds_by_matchers(matcher_list[1:], hwnd_parent=hwnd)
                if hwnd_list is None or len(hwnd_list) == 0:
                    return None
                hwnd_list_ret.append(hwnd)
                hwnd_list_ret.extend(hwnd_list)
            else:
                hwnd_list_ret.append(hwnd)
            return hwnd_list_ret
        except pywintypes.error as exp:
            print(exp)
    return None


def kill_process_by_name(p_name):
    for pid in psutil.pids():
        try:
            p = psutil.Process(pid)
            p_name_cur = p.name()
            if p_name_cur == p_name:
                print("找到进程", p_name_cur, "pid:", pid)
                # os.system("TASKKILL /F /IM 'League of Legends.exe'")
                os.kill(pid, 9)
                break
        except:
            logger.exception('结束进程失败')
            return -1

    return 0
# ------------------ 以上代码均出自其他模块点，主要为了自然关闭 shadow socks--------------------------


def start_sub_process(command_path):
    _, file_name = os.path.split(command_path)
    sub_process = subprocess.Popen(command_path)
    logger.info('进程已经开启')
    return sub_process


def close_sub_process_by_mouse():
    # 找到任务栏图标
    matcher_list = [('window', lambda x: win32gui.GetClassName(x).find('Shell_TrayWnd') == 0),
                    ('window', lambda x: win32gui.GetClassName(x).find('TrayNotifyWnd') == 0),
                    ('window', lambda x: win32gui.GetClassName(x).find('SysPager') == 0),
                    ('window', lambda x: win32gui.GetClassName(x).find('ToolbarWindow32') == 0 and
                                         win32gui.GetWindowText(x) == '用户提示通知区域'),
                    ]
    # hwnd_list = find_hwnds_by_lambdas(lambda_list)
    hwnd_list = find_hwnds_by_matchers(matcher_list)
    # 该列表有四个句柄，取 win32gui.GetWindowRect(0x100ea)  第一个坐标最靠右的一个
    hwnd_rect_dic = {hwnd: win32gui.GetWindowRect(hwnd) for hwnd in hwnd_list}
    max_rect_left = max([rect[0] for rect in hwnd_rect_dic.values()])
    rect_left, rect_top = 0, 0
    for hwnd_target, (rect_left, rect_top, _, _) in hwnd_rect_dic.items():
        if max_rect_left == rect_left:
            break
    # print(['%#x' % hwnd for hwnd in hwnd_list])
    # print('goto %d %d' % (rect_left, rect_top))
    # pyautogui.moveTo(rect_left + 10, rect_top + 10)
    # pyautogui.click(rect_left + 10, rect_top + 10, button='right')
    mouse_click(rect_left + 10, rect_top + 10, button='right')
    time.sleep(1)
    # pyautogui.moveTo(rect_left + 30, rect_top - 10)
    # pyautogui.click(rect_left + 30, rect_top - 10)
    mouse_click(rect_left - 30, rect_top - 10)
    logger.info('进程已经关闭')


def close_sub_process(sub_process: subprocess.Popen):
    if isinstance(sub_process, subprocess.Popen) and sub_process.returncode is None:
        # 这种方式非自然退出，将会导致无法浏览网页的情况
        # sub_process.send_signal(int(signal.SIGINT))
        sub_process.terminate()
        sub_process.wait()
        logger.info('进程已经关闭')


def get_price_latest():
    header = {
        'Content-Type': 'application/json',
        'X-CMC_PRO_API_KEY': 'f13a34ac-6460-4ffd-81fb-9805acf41902'
    }
    params = {
        # 'CMC_PRO_API_KEY': 'f13a34ac-6460-4ffd-81fb-9805acf41902',
        'limit': 5000,
        'start': 1
    }
    # https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?sort=market_cap&start=0&limit=10&cryptocurrency_type=tokens&convert=USD,BTC
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

    rsp = requests.get(url=url, params=params, headers=header)
    if rsp.status_code == 200:
        ret_dic = rsp.json()
        data_list = ret_dic['data']
        # print('len(data_list):', len(data_list))

        data_dic_list = []
        for dic in data_list:
            data_dic = {}
            for key, val in dic.items():
                if key == 'quote':
                    for sub_key, sub_val in val['USD'].items():
                        data_dic[sub_key] = sub_val
                else:
                    data_dic[key] = val
            data_dic_list.append(data_dic)

        df = pd.DataFrame(data_dic_list)
    else:
        raise ValueError('获取数据异常 %d\n%s', rsp.status_code, rsp.content)

    return df


def build_email(from_mail, to_mail_list, subject, attach_file_path=None):
    msg = MIMEMultipart()
    msg["Subject"] = Header(subject, "utf-8")
    msg["From"] = Header(from_mail, "utf-8")
    # msg["To"] = Header(",".join(to_mail_list), "utf-8")

    if attach_file_path is not None:
        _, file_name = os.path.split(attach_file_path)
        # 将xls作为附件添加到邮件中
        # 创建MIMEText对象，保存xls文件
        attach = MIMEText(open(attach_file_path, 'rb').read(), 'base64', 'utf-8')
        # 指定当前文件格式类型
        attach['Content-type'] = 'application/octet-stream'
        # 配置附件显示的文件名称,当点击下载附件时，默认使用的保存文件的名称
        # gb18030 qq邮箱中使用的是gb18030编码，防止出现中文乱码
        attach['Content-Disposition'] = 'attachment;filename="{file_name}"'.format(file_name=file_name)
        # 把附件添加到msg中
        msg.attach(attach)

    return msg


def send_email_qq(from_mail, to_mail_list, password, msg):
    smtp_server = "smtp.qq.com"
    smtp_port = 465
    # from_mail = "aaaaa@qq.com"
    # to_mail_list = ["bbbbb@qq.com"]
    # password = "****************"  # 16位授权码

    try:
        smtp = smtplib.SMTP_SSL(smtp_server, smtp_port)
        smtp.ehlo()
        # smtp.starttls()
        smtp.login(from_mail, password)
        smtp.sendmail(from_mail, to_mail_list, msg.as_string())
    except smtplib.SMTPException:
        logger.exception('发送邮件失败')
    # finally:
    #     smtp.quit()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s: %(levelname)s [%(name)s] %(message)s')
    from datetime import datetime
    import time

    command_path = r'd:\Softwares\Shadowsocks.exe'
    # command_path = r'D:\GitHub\new-pac\赛风3.exe'
    sub_process = start_sub_process(command_path)
    time.sleep(10)

    try:
        df = get_price_latest()

        file_name = 'latest_price_{0}.csv'.format(datetime.now().strftime('%y-%m-%d %H-%M-%S'))
        file_path = os.path.join(os.path.curdir, file_name)
        df.to_csv(file_path)
    finally:
        close_sub_process_by_mouse()
        # close_sub_process(sub_process)
        _, p_name = os.path.split(command_path)
        kill_process_by_name(p_name)
        pass

    # 将输出文件发送邮件
    # subject = 'CoinMarketCap 最新价格列表' + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # from_mail = '265590706@qq.com'
    # to_mail_list = ['mmmaaaggg@163.com', '1956044880@qq.com']
    # msg = build_email(from_mail, to_mail_list, subject, file_path)
    #
    # password = 'yvsqlyjpbhdmbghc'
    # send_email_qq(from_mail, to_mail_list, password, msg)
