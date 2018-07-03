# -*- coding: utf-8 -*-
"""
Created on 2017/9/29
@author: MG
"""


def clip(text: str, max_len: 'int > 0'=80) -> str:
    """
    在max_len前面或后面的第一个空格处截断文本
    :param text: 
    :param max_len: 
    :return: 
    """
    end = None
    if len(text) > max_len:
        space_before = text.rfind(' ', 0, max_len)
        if space_before >= 0:
            end = space_before
        else:
            space_after = text.rfind(' ', max_len)
            if space_after >= 0:
                end = space_after
    if end is None:  # 没找到空格
        end = len(text)
    return text[:end].rstrip()


if __name__ == "__main__":
    print(clip("12  3", 4))