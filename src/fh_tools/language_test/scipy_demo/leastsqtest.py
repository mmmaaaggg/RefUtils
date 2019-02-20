# -*- coding: utf-8 -*-
import numpy as np
from scipy.optimize import leastsq
import pylab as pl


def func_sin(x, p):
    """
    数据拟合所用的函数: A*sin(2*pi*k*x + theta)
    """
    A, k, theta = p
    return A*np.sin(2*np.pi*k*x+theta)


def func_line(x, p):
    """
    数据拟合所用的函数: A*sin(2*pi*k*x + theta)
    """
    A, k= p
    return A + k*x



x = np.linspace(0, -2*np.pi, 100)
A, k, theta = 10, 0.34, np.pi/6 # 真实数据的函数参数
y0 = func_sin(x, [A, k, theta]) # 真实数据
y1 = y0 + 2 * np.random.randn(len(x)) # 加入噪声之后的实验数据    

# ---------------------------------
# def residuals(p, y, x):
#     """
#     实验数据x, y和拟合函数之间的差，p为拟合需要找到的系数
#     """
#     return y - func_sin(x, p)
#
# p0 = [7, 0.2, 0] # 第一次猜测的函数拟合参数
#
# # 调用leastsq进行数据拟合
# # residuals为计算误差的函数
# # p0为拟合参数的初始值
# # args为需要拟合的实验数据
# plsq = leastsq(residuals, p0, args=(y1, x))
#
# print("真实参数:", [A, k, theta])
# print("拟合参数", plsq[0]) # 实验数据拟合后的参数
#
# # pl.plot(x, y0, label="真实数据")
# pl.plot(x, y1, label="带噪声的实验数据")
# pl.plot(x, func_sin(x, plsq[0]), label="拟合数据")
# pl.legend()
# pl.show()

# ---------------------------------
def residuals(p, y, x):
    """
    实验数据x, y和拟合函数之间的差，p为拟合需要找到的系数
    """
    return y - func_line(x, p)

p0 = [7, 0.2] # 第一次猜测的函数拟合参数

# 调用leastsq进行数据拟合
# residuals为计算误差的函数
# p0为拟合参数的初始值
# args为需要拟合的实验数据
plsq = leastsq(residuals, p0, args=(y1, x))

print("真实参数:", [A, k, theta])
print("拟合参数", plsq[0]) # 实验数据拟合后的参数

# pl.plot(x, y0, label="真实数据")
pl.plot(x, y1, label="带噪声的实验数据")
pl.plot(x, func_line(x, plsq[0]), label="拟合数据")
pl.legend()
pl.show()
