#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/8/22 9:21
@File    : send_email.py
@contact : mmmaaaggg@163.com
@desc    : 
"""
from datetime import datetime
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import os


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
    except smtplib.SMTPException as e:
        print(e.message)
    # finally:
    #     smtp.quit()


if __name__ == "__main__":
    subject = '带附件的测试邮件 ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    from_mail = '265590706@qq.com'
    to_mail_list = ['mmmaaaggg@163.com']
    attach_file_path = r'D:\WSPych\RefUtils\src\fh_tools\language_test\cryptocmd_test\latest_price_18-08-08 13-36-16.csv'
    msg = build_email(from_mail, to_mail_list, subject, attach_file_path)

    password = 'yvsqlyjpbhdmbghc'
    send_email_qq(from_mail, to_mail_list, password, msg)
