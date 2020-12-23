#! /usr/bin/env python3
"""
@author  : MG
@Time    : 2020/12/23 9:54
@File    : threading_save_lock_decorator.py
@contact : mmmaaaggg@163.com
@desc    : threading save decorator
"""
import threading
import time


def thread_save(func):
    lock = threading.Lock()

    def wrapper(*args, **kwargs):
        with lock:
            func(*args, **kwargs)

    return wrapper


@thread_save
def demo_func(user_name):
    print(f'{user_name} fall asleep')
    time.sleep(1)
    print(f'{user_name} has waken up')


def _test_func():
    for n in range(10):
        user_name = (' ' * n) + 'a'
        threading.Thread(target=demo_func, kwargs=dict(user_name=user_name)).start()

    print('wait all finished')
    time.sleep(11)
    print('all should finished')


if __name__ == "__main__":
    _test_func()
