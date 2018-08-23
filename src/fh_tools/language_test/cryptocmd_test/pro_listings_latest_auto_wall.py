#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/8/1 8:31
@File    : only_test.py
@contact : mmmaaaggg@163.com
@desc    : 
"""
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


def start_sub_process(command_path):
    _, file_name = os.path.split(command_path)
    sub_process = subprocess.Popen(command_path)
    logger.info('进程已经开启')
    return sub_process


def close_sub_process(sub_process):
    if isinstance(sub_process, subprocess.Popen) and sub_process.returncode is None:
        sub_process.kill()
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
        close_sub_process(sub_process)
        pass

    # 将输出文件发送邮件
    # subject = 'CoinMarketCap 最新价格列表' + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # from_mail = '265590706@qq.com'
    # to_mail_list = ['mmmaaaggg@163.com', '1956044880@qq.com']
    # msg = build_email(from_mail, to_mail_list, subject, file_path)
    #
    # password = 'yvsqlyjpbhdmbghc'
    # send_email_qq(from_mail, to_mail_list, password, msg)
