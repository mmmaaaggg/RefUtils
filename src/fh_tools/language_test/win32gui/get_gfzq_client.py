# -*- coding: utf-8 -*-
"""
Created on 2017/9/11
@author: MG
"""
import win32gui
from pprint import pprint
import re


def gbk2utf8(s):
    # return s.decode('gbk').encode('utf-8')
    return s.encode('utf-8')


def show_window_attr(hWnd):
    '''
    显示窗口的属性
    :return:
    '''
    if not hWnd:
        return

    # 中文系统默认title是gb2312的编码
    title = win32gui.GetWindowText(hWnd)
    title = gbk2utf8(title)
    clsname = win32gui.GetClassName(hWnd)

    print('窗口句柄:%s ' % (hWnd))
    print('窗口标题:%s' % (title))
    print('窗口类名:%s' % (clsname))
    print('')


def show_windows(hWndList):
    for h in hWndList:
        show_window_attr(h)


def is_gzzq_client(hWnd, hWndList):
    lpClassName_head = 'Afx:400000:0:0:'
    clsname = win32gui.GetClassName(hWnd)
    if re.match(r'Afx:400000:0:0:.+:0', clsname) is not None:
        hWndList.append(hWnd)


hWndList = []
# win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), hWndList)
win32gui.EnumWindows(is_gzzq_client, hWndList)
show_windows(hWndList)