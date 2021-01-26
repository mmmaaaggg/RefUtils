#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/8/22 9:21
@File    : send_email.py
@contact : mmmaaaggg@163.com
@desc    : 
"""
from email.mime.audio import MIMEAudio
from email.mime.image import MIMEImage
from typing import Optional
import mimetypes
from datetime import date
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders
import os


def build_email(from_mail, to_mail_list, subject, attach_file_path_list: Optional[list] = None):
    msg = MIMEMultipart()
    msg["Subject"] = Header(subject, "utf-8")
    # msg["From"] = Header(from_mail, "utf-8")
    msg["From"] = from_mail
    # msg["To"] = Header(",".join(to_mail_list), "utf-8")
    msg["To"] = ",".join(to_mail_list)

    if attach_file_path_list is not None:
        for attach_file_path in attach_file_path_list:
            ctype, encoding = mimetypes.guess_type(attach_file_path)
            if ctype is None or encoding is not None:
                ctype = 'application/octet-stream'

            maintype, subtype = ctype.split('/', 1)
            print("maintype, subtype", maintype, subtype)
            if maintype == 'text':
                with open(attach_file_path) as f:
                    mime = MIMEText(f.read(), _subtype=subtype)
            elif maintype == 'image':
                with open(attach_file_path, 'rb') as f:
                    mime = MIMEImage(f.read(), _subtype=subtype)
            elif maintype == 'audio':
                with open(attach_file_path, 'rb') as f:
                    mime = MIMEAudio(f.read(), _subtype=subtype)
            else:
                with open(attach_file_path, 'rb') as f:
                    mime = MIMEBase(maintype, subtype)
                    mime.set_payload(f.read())

            encoders.encode_base64(mime)
            _, file_name = os.path.split(attach_file_path)
            mime.add_header('Content-Disposition', 'attachment', filename=file_name)
            msg.attach(mime)

    return msg


def send_email_qq(from_mail, to_mail_list, password, msg):
    smtp_server = "smtp.qq.com"
    smtp_port = 465

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


def export_tables_and_send_email():
    subject = f'exports {date.today()}'
    from_mail = '265590706@qq.com'
    to_mail_list = ['mmmaaaggg@163.com']
    file_path_list = [f'd:\github\quant_vnpy\scripts\output\各策略持仓状态_2021-01-25.csv']
    msg = build_email(from_mail, to_mail_list, subject, file_path_list)

    # --- yvsqlyjpbhdmbghc ---
    password = '888'
    send_email_qq(from_mail, to_mail_list, password, msg)


if __name__ == "__main__":
    export_tables_and_send_email()
