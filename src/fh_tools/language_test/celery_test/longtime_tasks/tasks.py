#!/usr/bin/env python
# -*- coding:utf-8 -*-
import logging
from .celery import app
from .config import REDIS_HOST, REDIS_PORT, REDIS_DB_OTHER
import psutil
import time
import os
from redis import StrictRedis
logger = logging.getLogger()


@app.task
def add(x, y):
    if check_process_alive():
        logger.info('%d + %d waiting', x, y)
        return 0
    register_pid()
    logger.info('%d + %d runing', x, y)
    ret = x + y
    time.sleep(ret)
    logger.info('%d + %d = %d task finished', x, y, ret)
    return ret


def register_pid():
    r = StrictRedis(REDIS_HOST, REDIS_PORT, db=REDIS_DB_OTHER)
    key = "task_add_pid"
    pid = os.getpid()
    r.set(key, pid)


def check_process_alive():
    r = StrictRedis(REDIS_HOST, REDIS_PORT, db=REDIS_DB_OTHER)
    key = "task_add_pid"
    pid = r.get(key)
    is_alive = False
    if pid is None:
        logger.warning('No pid')
        return is_alive
    r.set(key, pid)
    try:
        pinfo = psutil.Process(int(pid))
        is_alive = pinfo.is_running()
        logger.info('%s=%r is alive: %s', key, pid, is_alive)
    except psutil.NoSuchProcess:
        logger.info('%s=%r is alive: %s (not exist)', key, pid, is_alive)
    finally:
        return is_alive

if __name__ == '__main__':
    # get pid
    r = StrictRedis(REDIS_HOST, REDIS_PORT, db=REDIS_DB_OTHER)
    key = "task_add_pid"
    pid = r.get(key)
    if pid is None:
        print('get new pid')
        pid = os.getpid()
    print('%s : %s' % (key, str(pid)))
    r.set(key, pid)
    print(os.getpid())
    try:
        pinfo = psutil.Process(int(pid))
        print('pinfo.is_running()', pinfo.is_running())
    except psutil.NoSuchProcess:
        pinfo = psutil.Process(int(os.getpid()))
        print('current pinfo.is_running()', pinfo.is_running())