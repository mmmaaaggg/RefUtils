# -*- coding: utf-8 -*-
"""
Created on 2017/9/19
@author: MG
"""
import win32gui
import re
from functools import partial


# def _filter_trade_client(hwnd, hwnd_list, filter_func):
#     if filter_func(hwnd):
#         hwnd_list.append(hwnd)


def filter_func(hwnd):
    # 找到classname = '#32770' 的窗体
    re_classname_pattern = 'ToolbarWindow32'
    clsname = win32gui.GetClassName(hwnd)
    if re.match(re_classname_pattern, clsname) is None:
        return False
    # 找到 窗体标题为 “提示”的窗体
    hwnd_chld_list = []
    try:
        win32gui.EnumChildWindows(hwnd, lambda hwnd_sub, hwnd_chld_list_tmp: hwnd_chld_list_tmp.append(hwnd_sub),
                                  hwnd_chld_list)
        for hwnd_sub in hwnd_chld_list:
            if win32gui.GetClassName(hwnd_sub) == 'Static' and win32gui.GetWindowText(hwnd_sub) == '提示':
                return True
    except:
        pass
    return False


def find_window_whnd(filter_func, ret_first=True):
    # 输入 filter_func 查找符合条件的全部或首个窗口whnd
    window_hwnd = None
    hwnd_list = []
    win32gui.EnumWindows(lambda hwnd, hwnd_list_tmp: hwnd_list_tmp.append(hwnd) if filter_func(hwnd) else hwnd,
                         hwnd_list)
    if len(hwnd_list) > 0:
        if ret_first:
            window_hwnd = hwnd_list[0]
            return window_hwnd
        else:
            return hwnd_list
    else:
        return None


def filter_hwnd_func(hwnd, contain_window_text):
    """ 查找 内部包含“contain_window_text”标签的框体"""
    try:
        # 找到classname = '#32770' 的窗体
        re_classname_pattern = '#32770'
        clsname = win32gui.GetClassName(hwnd)
        if re.match(re_classname_pattern, clsname) is None:
            return False
        # 查找 内部包含“可用金额”标签的框体
        hwnd_chld_list = []
        win32gui.EnumChildWindows(hwnd, lambda hwnd_sub, hwnd_chld_list_tmp: hwnd_chld_list_tmp.append(hwnd_sub),
                                  hwnd_chld_list)
        for hwnd_sub in hwnd_chld_list:
            if win32gui.GetClassName(hwnd_sub) == 'Static' and win32gui.GetWindowText(hwnd_sub) == contain_window_text:
                return True
    except:
        pass
    return False


def filter_by_win_title(hwnd, contain_window_text):
    """ 查找 内部包含“contain_window_text”标签的框体"""
    clsname = win32gui.GetClassName(hwnd)
    return contain_window_text == clsname


if __name__ == "__main__":
    # hwnd_list = find_window_whnd(filter_func, ret_first=False)
    # print([(hwnd, hex(hwnd)) for hwnd in hwnd_list])
    hwnd = find_window_whnd(filter_func, ret_first=True)
    print("hwnd:%d [%s]" % (hwnd, hex(hwnd)))