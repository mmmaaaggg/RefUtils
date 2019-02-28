#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/12/11 10:16
@File    : ftt_test.py
@contact : mmmaaaggg@163.com
@desc    : 原文：https://blog.csdn.net/ouening/article/details/71079535
傅里叶变换
"""

import numpy as np
from scipy.fftpack import fft, ifft
import matplotlib.pyplot as plt
import seaborn

# 采样点选择1400个，因为设置的信号频率分量最高为600赫兹，根据采样定理知采样频率要大于信号频率2倍，所以这里设置采样频率为1400赫兹（即一秒内有1400个采样点，一样意思的）
x = np.linspace(0, 1, 1400)

# 设置需要采样的信号，频率分量有180，390和600
y = 7 * np.sin(2 * np.pi * 180 * x) + 2.8 * np.sin(2 * np.pi * 390 * x) + 5.1 * np.sin(2 * np.pi * 600 * x)

yy = fft(y)  # 快速傅里叶变换
yreal = yy.real  # 获取实数部分
yimag = yy.imag  # 获取虚数部分

yf = abs(fft(y))  # 取绝对值
yf1 = abs(fft(y)) / len(x)  # 归一化处理
yf2 = yf1[range(int(len(x) / 2))]  # 由于对称性，只取一半区间

xf = np.arange(len(y))  # 频率
xf1 = xf
xf2 = xf[range(int(len(x) / 2))]  # 取一半区间

plt.subplot(321)
plt.plot(x[0:100], y[0:100])
plt.title('Original wave')

plt.subplot(322)
plt.plot(yreal, yimag, 'b')
plt.title('yreal vs yimag)', fontsize=10, color='#F08080')

plt.subplot(323)
plt.plot(xf, yf, 'r')
plt.title('FFT of Mixed wave(two sides frequency range)', fontsize=7, color='#7A378B')  # 注意这里的颜色可以查询颜色代码表

plt.subplot(324)
plt.plot(xf1, yf1, 'g')
plt.title('FFT of Mixed wave(normalization)', fontsize=9, color='r')

plt.subplot(325)
plt.plot(xf2, yf2, 'b')
plt.title('FFT of Mixed wave)', fontsize=10, color='#F08080')

# for freq, qual in [(num, x) for num, x in enumerate(yf2) if x > 1]:
#     print(freq, qual)


def get_func(freq_amplitude_list: list):
    """将傅里叶变换 频率 + 相位 list 转换为函数"""
    def func(x):
        ret = None
        for freq, amplitude in freq_amplitude_list:
            if ret is None:
                ret = np.sin(2 * np.pi * freq * x) * amplitude
            else:
                ret += np.sin(2 * np.pi * freq * x) * amplitude
        return ret

    return func


yff = get_func([(num, xx) for num, xx in enumerate(yf2) if xx > 1])(x)
plt.subplot(326)
plt.plot(x[0:100], yff[0:100], 'b')
plt.title('FFT transferred line)', fontsize=10, color='#F08000')

plt.show()
