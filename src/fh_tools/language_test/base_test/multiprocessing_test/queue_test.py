#! /usr/bin/env python3
"""
@author  : MG
@Time    : 2020/10/25 下午8:44
@File    : queue_test.py
@contact : mmmaaaggg@163.com
@desc    :
"""
import time
from queue import Empty
import multiprocessing
from multiprocessing import JoinableQueue  # It's different from "from multiprocessing.queues import JoinableQueue"
from multiprocessing.pool import Pool


def func(queue: JoinableQueue, n):
    print("process", n)
    time.sleep(n)
    try:
        _ = queue.get(block=True, timeout=10)
        time.sleep(_)
        queue.task_done()
    except Empty:
        print("empty!!")

    print("process", n, 'end')
    return n


def _test_():
    # windows 启动方式
    # multiprocessing.set_start_method('spawn')
    # 获取上下文
    # ctx = multiprocessing.get_context('spawn')
    # 检查这是否是冻结的可执行文件中的伪分支进程。
    # ctx.freeze_support()
    manager = multiprocessing.Manager()

    pool = Pool(3)
    queue = manager.Queue()
    print("start process 1")
    pool.apply_async(func, args=(queue, 1))
    print("start process 2")
    pool.apply_async(func, args=(queue, 2))
    print("start process 3")
    pool.apply_async(func, args=(queue, 3))
    print("all process started")
    queue.put(1)
    queue.put(2)
    queue.put(3)
    print('queue put finished and join until finished')
    # time.sleep(3)
    # try:
    #     _ = queue.get()
    #     print("has value", _)
    #     queue.task_done()
    #
    # except Empty:
    #     print("empty on main process")
    #
    # try:
    #     _ = queue.get()
    #     print("has value", _)
    #     queue.task_done()
    #
    # except Empty:
    #     print("empty on main process")
    #
    # try:
    #     _ = queue.get()
    #     print("has value", _)
    #     queue.task_done()
    #
    # except Empty:
    #     print("empty on main process")

    queue.join()
    print('all task done')


if __name__ == "__main__":
    _test_()
