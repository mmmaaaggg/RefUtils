#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2019/02/20 下午3:59
@File    : nelder-mead
@contact : mmmaaaggg@163.com
@desc    : 作为寻优的目标函数来简要介绍在SciPy中使用优化模块scipy.optimize nelder-mead
"""
import numpy as np
from scipy import optimize as opt

# 首先需要定义一下这个Rosenbrock函数：
def rosen(x):
    """The Rosenbrock function"""
    return sum(100.0*(x[1:]-x[:-1]**2.0)**2.0 + (1-x[:-1])**2.0)
# 3.1.1 Nelder-Mead单纯形法
# 单纯形法是运筹学中介绍的求解线性规划问题的通用方法，
# 这里的Nelder-Mead单纯形法与其并不相同，只是用到单纯形的概念。
# 设定起始点x0=(1.3,0.7,0.8,1.9,1.2)，并进行最小化的寻优。
# 这里xtol表示迭代收敛的容忍误差上界：
x_0 = np.array([0.5, 1.6, 1.1, 0.8, 1.2])
res = opt.minimize(rosen, x_0, method='nelder-mead', options={'xtol': 1e-8, 'disp': True})
print("Result of minimizing Rosenbrock function via Nelder-Mead Simplex algorithm:")
print(res)

# Optimization terminated successfully.
#          Current function value: 0.000000
#          Iterations: 436
#          Function evaluations: 706
# Result of minimizing Rosenbrock function via Nelder-Mead Simplex algorithm:
#   status: 0
#     nfev: 706
#  success: True
#      fun: 1.6614969876635003e-17
#        x: array([ 1.,  1.,  1.,  1.,  1.])
#  message: 'Optimization terminated successfully.'
#      nit: 436
# Rosenbrock函数的性质比较好，简单的优化方法就可以处理了，
# 还可以在minimize中使用method='powell'来指定使用Powell's method。
# 这两种简单的方法并不使用函数的梯度，在略微复杂的情形下收敛速度比较慢，下面让我们来看一下用到函数梯度进行寻优的方法。
