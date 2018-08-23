#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/8/22 13:24
@File    : close_process_by_name.py
@contact : mmmaaaggg@163.com
@desc    : 
"""
import os
import psutil
import signal
import logging

logger = logging.getLogger()


def is_process_exist(p_name):
    for pid in psutil.pids():
        p = psutil.Process(pid)
        p_name_cur = p.name()
        if p_name_cur == p_name:
            print("找到进程", p_name_cur, "pid:", pid)
            # os.system("TASKKILL /F /IM 'League of Legends.exe'")
            return True

    return False


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


if __name__ == "__main__":
    p_name = 'Shadowsocks.exe'
    kill_process_by_name(p_name)
