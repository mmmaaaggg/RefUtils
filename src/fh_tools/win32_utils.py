# -*- coding: utf-8 -*-
"""
Created on 2017/4/12
@author: MG
"""
import win32api
import win32con
import win32gui
import pywintypes
import pyautogui
import time
from ctypes import windll


def find_hwnds_by_lambdas(lambda_list, hwnd_parent=None):
    """
    通过子控件标题栏内容找到对应控件
    :param lambda_list:  lambda 列表
    :param hwnd_parent:  母窗体 ID
    :return:  返回窗体ID列表，如果有任意一项不匹配，则返回 None
    """
    hwnd_list_ret = []
    lambda_count = len(lambda_list)
    if lambda_count == 0:
        return None
    func = lambda_list[0]
    exp_count = 0
    hwnd = None
    while hwnd is None or hwnd != 0:
        hwnd = win32gui.FindWindowEx(hwnd_parent, hwnd, None, None)
        if hwnd == 0:
            break
        is_ok = func(hwnd)
        if is_ok:
            hwnd_list_ret.append(hwnd)
            if lambda_count > 1:
                hwnd_list = find_hwnds_by_lambdas(lambda_list[1:], hwnd_parent=hwnd)
                if hwnd_list is None or len(hwnd_list) == 0:
                    continue
                hwnd_list_ret.extend(hwnd_list)
            return hwnd_list_ret
    return None


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


def mouse_move(x, y):
    windll.user32.SetCursorPos(x, y)


def mouse_click(x=None, y=None):
    if not x is None and not y is None:
        mouse_move(x, y)
        time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


if __name__ == '__main__':
    # 以恒泰证券交易端界面为测试用例
    # matcher_list = [('window', lambda x: win32gui.GetClassName(x).find('Afx:400000') == 0),
    #                 ('window', lambda x: win32gui.GetClassName(x).find('Afx:400000') == 0),
    #                 ('DlgItem', 0xE900),
    #                 ('DlgItem', 0xE900),
    #                 ('DlgItem', 0x81),
    #                 ('DlgItem', 0xC8),
    #                 ('DlgItem', 0x81),
    #                 ]
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
    for hwnd_target, (rect_left, rect_top, _, _) in hwnd_rect_dic.items():
        if max_rect_left == rect_left:
            break
    print(['%#x' % hwnd for hwnd in hwnd_list])
    print('goto %d %d' % (rect_left, rect_top))
    # pyautogui.moveTo(rect_left + 10, rect_top + 10)
    pyautogui.click(rect_left + 10, rect_top + 10, button='right')
    time.sleep(1)
    # pyautogui.moveTo(rect_left + 30, rect_top - 10)
    # pyautogui.click(rect_left + 30, rect_top - 10)
    mouse_click(rect_left - 30, rect_top - 10)

