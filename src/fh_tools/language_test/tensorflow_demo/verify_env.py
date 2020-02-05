#! /usr/bin/env python3
"""
@author  : MG
@Time    : 2020/2/5 上午8:59
@File    : verify_env.py
@contact : mmmaaaggg@163.com
@desc    : 验证 tensorflow 2.1.0 环境是否安装正常
"""

if __name__ == "__main__":
    import tensorflow as tf
    print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))
