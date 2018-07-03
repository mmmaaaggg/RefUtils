#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/6/22 16:21
@File    : try_n_times.py
@contact : mmmaaaggg@163.com
@desc    : 
"""
import functools
import logging
import time
_logger = logging.getLogger()


def try_n_times(times=3, sleep_time=3, logger: logging.Logger=None):
    """
    尝试最多 times 次，异常捕获记录后继续尝试
    :param times:
    :param sleep_time:
    :param logger: 如果异常需要 log 记录则传入参数
    :return:
    """
    last_invoked_time = [None]

    def wrap_func(func):

        @functools.wraps(func)
        def try_it(*arg, **kwargs):
            for n in range(1, times+1):
                if sleep_time > 0 and last_invoked_time[0] is not None\
                        and (time.time() - last_invoked_time[0]) < sleep_time:
                    time.sleep(sleep_time - (time.time() - last_invoked_time[0]))

                try:
                    ret_data = func(*arg, **kwargs)
                except:
                    if logger is not None:
                        logger.exception("第 %d 次调用 %s 出错", n, func.__name__)
                    continue
                finally:
                    last_invoked_time[0] = time.time()

                break
            else:
                ret_data = None

            return ret_data

        return try_it

    return wrap_func


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(name)s %(filename)s.%(funcName)s:%(lineno)d|%(message)s')
    counter_dic = {1: 1}

    def counter():
        num = counter_dic[1]
        counter_dic[1] = num + 1
        return num


    @try_n_times(3, 3, _logger)
    def foo(nths):
        if counter() in nths:
            raise ValueError('')
        else:
            return 'ok'

    print("foo(1)", foo([1, 2]))

