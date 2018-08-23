#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/8/22 13:36
@File    : with_sub_process.py
@contact : mmmaaaggg@163.com
@desc    : 
"""

import subprocess
import logging

logger = logging.getLogger()


def start_sub_process(command_path):
    sub_process = subprocess.Popen(command_path)
    logger.info('进程已经开启')
    return sub_process


def close_sub_process(sub_process):
    if isinstance(sub_process, subprocess.Popen) and sub_process.returncode == None:
        sub_process.kill()
        sub_process.wait()
        logger.info('进程已经关闭')


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s: %(levelname)s [%(name)s] %(message)s')
    import time

    command_path = r'd:\Softwares\Shadowsocks.exe'
    sub_process = start_sub_process(command_path)
    time.sleep(15)
    close_sub_process(sub_process)
