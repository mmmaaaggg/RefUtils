# -*- coding: utf-8 -*-
"""
Created on 2017/9/1
@author: MG
"""
import time, os, psutil, signal


while True:
    p_name1 = 'LeagueClient.exe'  # "QQ.exe"
    p_name2 = 'LeagueClientUxRender.exe'  # "QQ.exe"
    for pid in psutil.pids():
        try:
            p = psutil.Process(pid)
            p_name = p.name()
            if p_name == p_name1 or p_name == p_name2:
                # print("找到进程", p.name(), "pid:", pid)
                time.sleep(1200)
                # os.system("TASKKILL /F /IM 'League of Legends.exe'")
                os.kill(pid, 9)
                break
        except:
            pass

    time.sleep(60)
