#! /usr/bin/env python3
"""
@author  : MG
@Time    : 2020/4/5 上午10:35
@File    : gradiant_decent.py
@contact : mmmaaaggg@163.com
@desc    : 
"""
import math
import numpy as np


def func(x):
    return -math.exp(-(x[0] ** 2 + x[1] ** 2))


def grad_func(x):
    return np.array([2 * x[0] * math.exp(-(x[0] ** 2 + x[1] ** 2)),
                     2 * x[1] * math.exp(-(x[0] ** 2 + x[1] ** 2))])


def gradient_descent(grad, x=np.array([1.0, -1.0], dtype=np.float64),
                     learning_rate=0.5, precision=1e-7, max_iters=10000):
    print(f"初始值{x}")
    for i in range(max_iters):
        diff = grad(x)
        if np.linalg.norm(diff, ord=2) < precision:
            break
        x -= diff * learning_rate
        print(f"第{i:4d}轮迭代 diff=[{diff[0]:.9f}, {diff[1]:.10f}] x=[{x[0]:.9f}, {x[1]:.10f}]")

    print(f'最优解 {x}')


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    # xs = np.linspace(-2, 2)
    # ys = np.exp(-(xs ** 2))
    # grads = -2 * xs * np.exp(-(xs ** 2))
    # plt.plot(xs, ys, xs, grads)
    # plt.show()
    gradient_descent(grad_func, x=np.array([2, -2], dtype=np.float64))
    # gradient_descent(grad_func, x=np.array([3.2, -3.2], dtype=np.float64))
