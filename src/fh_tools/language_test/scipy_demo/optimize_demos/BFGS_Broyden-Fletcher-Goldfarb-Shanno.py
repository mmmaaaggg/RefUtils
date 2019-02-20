#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2019/02/20 下午4:11
@File    : BFGS_Broyden-Fletcher-Goldfarb-Shanno
@contact : mmmaaaggg@163.com
@desc    : Broyden-Fletcher-Goldfarb-Shanno（BFGS）法用到了梯度信息
"""
from scipy import optimize as opt
import numpy as np

# 首先需要定义一下这个Rosenbrock函数：
def rosen(x):
    """The Rosenbrock function"""
    return sum(100.0*(x[1:]-x[:-1]**2.0)**2.0 + (1-x[:-1])**2.0)

x_0 = np.array([0.5, 1.6, 1.1, 0.8, 1.2])

# 我们可以如下定义梯度向量的计算函数了：
def rosen_der(x):
    xm = x[1:-1]
    xm_m1 = x[:-2]
    xm_p1 = x[2:]
    der = np.zeros_like(x)
    der[1:-1] = 200*(xm-xm_m1**2) - 400*(xm_p1 - xm**2)*xm - 2*(1-xm)
    der[0] = -400*x[0]*(x[1]-x[0]**2) - 2*(1-x[0])
    der[-1] = 200*(x[-1]-x[-2]**2)
    return der
# 梯度信息的引入在minimize函数中通过参数jac指定：
res = opt.minimize(rosen, x_0, method='BFGS', jac=rosen_der, options={'disp': True})
print("Result of minimizing Rosenbrock function via Broyden-Fletcher-Goldfarb-Shanno algorithm:")
print(res)

# Optimization terminated successfully.
#          Current function value: 0.000000
#          Iterations: 52
#          Function evaluations: 63
#          Gradient evaluations: 63
# Result of minimizing Rosenbrock function via Broyden-Fletcher-Goldfarb-Shanno algorithm:
#    status: 0
#   success: True
#      njev: 63
#      nfev: 63
#  hess_inv: array([[ 0.00726515,  0.01195827,  0.0225785 ,  0.04460906,  0.08923649],
#        [ 0.01195827,  0.02417936,  0.04591135,  0.09086889,  0.18165604],
#        [ 0.0225785 ,  0.04591135,  0.09208689,  0.18237695,  0.36445491],
#        [ 0.04460906,  0.09086889,  0.18237695,  0.36609277,  0.73152922],
#        [ 0.08923649,  0.18165604,  0.36445491,  0.73152922,  1.46680958]])
#       fun: 3.179561068096293e-14
#         x: array([ 1.        ,  0.99999998,  0.99999996,  0.99999992,  0.99999983])
#   message: 'Optimization terminated successfully.'
#       jac: array([  4.47207141e-06,   1.30357917e-06,  -1.86454207e-07,
#         -2.00564982e-06,   4.98799446e-07])
