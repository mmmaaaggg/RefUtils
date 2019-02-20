#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2019/02/20 下午4:15
@File    : Newton-CG_Newton-Conjugate-Gradient algorithm
@contact : mmmaaaggg@163.com
@desc    : Newton-CG_Newton-Conjugate-Gradient algorithm
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

# 用到梯度的方法还有牛顿法，牛顿法是收敛速度最快的方法，其缺点在于要求Hessian矩阵（二阶导数矩阵）。
# 牛顿法大致的思路是采用泰勒展开的二阶近似：
# 为使用牛顿共轭梯度法，我们需要提供一个计算Hessian矩阵的函数：


def rosen_hess(x):
    x = np.asarray(x)
    H = np.diag(-400*x[:-1],1) - np.diag(400*x[:-1],-1)
    diagonal = np.zeros_like(x)
    diagonal[0] = 1200*x[0]**2-400*x[1]+2
    diagonal[-1] = 200
    diagonal[1:-1] = 202 + 1200*x[1:-1]**2 - 400*x[2:]
    H = H + np.diag(diagonal)
    return H


res = opt.minimize(rosen, x_0, method='Newton-CG', jac=rosen_der, hess=rosen_hess, options={'xtol': 1e-8, 'disp': True})
print("Result of minimizing Rosenbrock function via Newton-Conjugate-Gradient algorithm (Hessian):")
print(res)

# Optimization terminated successfully.
#          Current function value: 0.000000
#          Iterations: 20
#          Function evaluations: 22
#          Gradient evaluations: 41
#          Hessian evaluations: 20
# Result of minimizing Rosenbrock function via Newton-Conjugate-Gradient algorithm:
#   status: 0
#  success: True
#     njev: 41
#     nfev: 22
#      fun: 1.47606641102778e-19
#        x: array([ 1.,  1.,  1.,  1.,  1.])
#  message: 'Optimization terminated successfully.'
#     nhev: 20
#      jac: array([ -3.62847530e-11,   2.68148992e-09,   1.16637362e-08,
#          4.81693414e-08,  -2.76999090e-08])
# 对于一些大型的优化问题，Hessian矩阵将异常大，牛顿共轭梯度法用到的仅是Hessian矩阵和一个任意向量的乘积，
# 为此，用户可以提供两个向量，一个是Hessian矩阵和一个任意向量p的乘积，另一个是向量p，这就减少了存储的开销。
# https://wizardforcel.gitbooks.io/python-quant-uqer/8.html
