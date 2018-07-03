# -*- coding: utf-8 -*-
"""
Created on 2017/9/12
@author: MG
"""
import win32gui
import win32con


def get_text_by_hwnd(hwnd, buffer_len=100):
    buffer = win32gui.PyMakeBuffer(buffer_len)
    length = win32gui.SendMessage(hwnd, win32con.WM_GETTEXT, buffer_len, buffer)
    buf_len = length * 2 if length * 2 < 100 else 100
    aaa = [chr(buf) for buf in buffer[:buf_len] if buf != 0]
    char_list = []
    for n_buf, a_byte in enumerate(buffer[:buf_len]):
        if n_buf % 2 != 0:
            continue
        if a_byte == 0:
            break
        char_list.append(chr(a_byte))
        # print(buf, chr(buf))
    ret_str = ''.join(char_list)
    return ret_str

hwnd = 0x00410A50
buffer_len = 100
ret_str = get_text_by_hwnd(hwnd, buffer_len)
print(ret_str)
