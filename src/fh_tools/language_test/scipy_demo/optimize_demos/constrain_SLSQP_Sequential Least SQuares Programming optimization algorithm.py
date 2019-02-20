#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2019/02/20 下午4:23
@File    : constrain_SLSQP_Sequential Least SQuares Programming optimization algorithm
@contact : mmmaaaggg@163.com
@desc    : 3.2约束优化问题 constrain_SLSQP_Sequential Least SQuares Programming optimization algorithm
"""
from scipy import optimize as opt
import numpy as np

# 定义目标函数及其导数为：


def func(x, sign=1.0):
    """ Objective function """
    return sign*(2*x[0]*x[1] + 2*x[0] - x[0]**2 - 2*x[1]**2)


def func_deriv(x, sign=1.0):
    """ Derivative of objective function """
    dfdx0 = sign*(-2*x[0] + 2*x[1] + 2)
    dfdx1 = sign*(2*x[0] - 4*x[1])
    return np.array([ dfdx0, dfdx1 ])

# 其中sign表示求解最小或者最大值，我们进一步定义约束条件：


cons = ({'type': 'eq',  'fun': lambda x: np.array([x[0]**3 - x[1]]), 'jac': lambda x: np.array([3.0*(x[0]**2.0), -1.0])},
      {'type': 'ineq', 'fun': lambda x: np.array([x[1] - 1]), 'jac': lambda x: np.array([0.0, 1.0])})

# 最后我们使用SLSQP（Sequential Least SQuares Programming optimization algorithm）方法进行约束问题的求解
# （作为比较，同时列出了无约束优化的求解）：

res = opt.minimize(func, [-1.0, 1.0], args=(-1.0,), jac=func_deriv, method='SLSQP', options={'disp': True})
print("Result of unconstrained optimization:")
print(res)
res = opt.minimize(func, [-1.0, 1.0], args=(-1.0,), jac=func_deriv, constraints=cons, method='SLSQP', options={'disp': True})
print("Result of constrained optimization:")
print(res)

# Optimization terminated successfully.    (Exit mode 0)
#             Current function value: -2.0
#             Iterations: 4
#             Function evaluations: 5
#             Gradient evaluations: 4
# Result of unconstrained optimization:
#   status: 0
#  success: True
#     njev: 4
#     nfev: 5
#      fun: -1.9999999999999996
#        x: array([ 2.,  1.])
#  message: 'Optimization terminated successfully.'
#      jac: array([ -2.22044605e-16,  -0.00000000e+00,   0.00000000e+00])
#      nit: 4
# Optimization terminated successfully.    (Exit mode 0)
#             Current function value: -1.00000018311
#             Iterations: 9
#             Function evaluations: 14
#             Gradient evaluations: 9
# Result of constrained optimization:
#   status: 0
#  success: True
#     njev: 9
#     nfev: 14
#      fun: -1.0000001831052137
#        x: array([ 1.00000009,  1.        ])
#  message: 'Optimization terminated successfully.'
#      jac: array([-1.99999982,  1.99999982,  0.        ])
#      nit: 9
