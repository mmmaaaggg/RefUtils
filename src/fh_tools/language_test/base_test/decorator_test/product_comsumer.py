#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/6/14 9:34
@File    : product_comsumer.py
@contact : mmmaaaggg@163.com
@desc    : 
"""


def bulk_invoke(func):
    print('bulk func')
    a = []

    def bulk_func(n):
        a.append(n)
        if len(a) > 3:
            func(a)
            a.clear()

    return bulk_func


@bulk_invoke
def fprint(n):
    print(n)


class DCTest:
    def __init__(self):
        print('create decorator')

    def __call__(self, func):
        print('get func', func.__name__)
        self._func = func

        def _call(*args, **kwargs):
            print('call func', args, kwargs)
            self._func(*args, **kwargs)

        return _call



@DCTest()
def fprint2(n):
    print(n)


from queue import Queue, Empty
from threading import Thread
from datetime import datetime, timedelta
import time


class ProducerConsumer(Thread):
    """
    实现生产者-消费者模式，被装饰函数将变为被异步调用
    """
    def __init__(self, threshold=100, interval=3, pass_arg_list=True, is_class_method=False):
        super().__init__(daemon=True)
        self.queue = Queue()
        self.threshold = threshold
        self.interval = interval
        self.pass_arg_list = pass_arg_list
        self.is_class_method = is_class_method
        self.func = []

    def __call__(self, func):
        # 通过 [func] 方式进行保存，是为了防止调用的时候讲当前对象传递进去
        self.func = [func]
        self.name = func.__name__

        def _call(*args, **kwargs):
            print('call ', func.__name__, *args, **kwargs)
            if not self.is_alive():
                print('start worker thread')
                self.start()
            self.queue.put_nowait((args, kwargs))
            # self._func(*args, **kwargs)

        return _call

    def run(self):
        if len(self.func) != 1:
            return

        func = self.func[0]
        if self.pass_arg_list:
            # 类方法对象为key 而进行分组调用
            class_method_args_dic, self_obj_key = {}, ''

            # args_list = []
            # kwargs_list_dic = {}
            # args_len = 0
            datetime_last_invoke = datetime.now()
            while True:
                try:
                    args_tmp, kwargs_tmp = self.queue.get(timeout=5)
                    # 获取对象
                    if self.is_class_method:
                        self_obj_key = args_tmp[0]
                        args_tmp = args_tmp[1:]

                    # 获取相关参数列表
                    args_list, kwargs_list_dic, datetime_last_invoke = class_method_args_dic.setdefault(
                        self_obj_key, [[], {}, datetime.now()])
                    args_len = len(args_list)
                    # print("args_tmp:", args_tmp)
                    for num, arg in enumerate(args_tmp):
                        # print(num, ")arg:", arg, "|", len(args), ')args:', args)
                        if len(args_list) <= num:
                            # 保持所有参数对齐，避免出现新增参数，与旧参数错位的情况
                            new_arg = [None for _ in range(args_len)]
                            new_arg.append(arg)
                            args_list.append(new_arg)
                        else:
                            args_list[num].append(arg)

                    for key, arg in kwargs_tmp.items():
                        # 保持所有参数对齐，避免出现新增参数，与旧参数错位的情况
                        kwargs_list_dic.setdefault(key, [None for _ in range(args_len)]).append(arg)

                except Empty:
                    pass

                args_len = len(args_list)
                if args_len > 0 and (args_len >= self.threshold or (
                        datetime.now() - datetime_last_invoke).seconds >= self.interval):
                    print('start real call -> self_obj_key, args_list, kwargs_list_dic:',
                          self_obj_key, args_list, kwargs_list_dic)
                    if self.is_class_method:
                        func(self_obj_key, *args_list, **kwargs_list_dic)
                    else:
                        func(*args_list, **kwargs_list_dic)
                    args_list.clear()
                    for _, v in kwargs_list_dic.items():
                        v.clear()

                    class_method_args_dic[self_obj_key][2] = datetime.now()
        else:
            args_list = []
            kwargs_list = []
            args_len = 0
            datetime_last_invoke = datetime.now()
            while True:
                try:
                    args_tmp, kwargs_tmp = self.queue.get(timeout=5)
                    # print("args_tmp:", args_tmp)
                    args_list.append(args_tmp)
                    kwargs_list.append(kwargs_tmp)

                    args_len += 1

                except Empty:
                    pass

                if args_len > 0 and (args_len >= self.threshold or (
                        datetime.now() - datetime_last_invoke).seconds >= self.interval):
                    # print("args_list, kwargs_list", args_list, kwargs_list)
                    for args, kwargs in zip(args_list, kwargs_list):
                        # print("args, kwargs", args, kwargs)
                        func(*args, **kwargs)
                        args_list = []
                        kwargs_list = []
                        args_len = 0
                        datetime_last_invoke = datetime.now()


@ProducerConsumer(threshold=3)
def print_list(n):
    print('print_list', n)


@ProducerConsumer(threshold=3, pass_arg_list=False)
def print_n(n):
    print('print_n', n)


class AClass:

    @ProducerConsumer(threshold=3, is_class_method=True)
    # @DCTest()
    def print_method(self, n):
        print(self.__class__.__name__, "print_method", n)


if __name__ == "__main__":
    # for n in range(10):
    #     print_list(n)
    #
    # for n in range(10):
    #     print_n(n)

    aaa = AClass()
    for n in range(10):
        time.sleep(1)
        aaa.print_method(n)
    time.sleep(6)
