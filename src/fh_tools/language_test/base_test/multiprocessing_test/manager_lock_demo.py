#! /usr/bin/env python3
"""
@author  : MG
@Time    : 2020/10/31 上午5:45
@File    : manager_lock_demo.py
@contact : mmmaaaggg@163.com
@desc    : 演示 manager.Lock() 使用方法
"""
import time

from multiprocessing import Pool, Manager, Lock


def sub_process(name, lock: Lock):
    print('%s get task' % name)
    with lock:
        print('%s doing task on %s %s' % (name, lock, type(lock)))
        time.sleep(3)

    print('%s finish task' % name)


def main_process(multi_process=3):
    print("启动进程池")

    pool = Pool(processes=multi_process)
    manager = Manager()
    lock = manager.Lock()
    pool.apply_async(sub_process, args=('process1', lock))
    pool.apply_async(sub_process, args=('process2', lock))
    pool.apply_async(sub_process, args=('process3', lock))
    pool.apply_async(sub_process, args=('process4', lock))
    pool.close()
    pool.join()
    print('all finished')


if __name__ == "__main__":
    main_process()
