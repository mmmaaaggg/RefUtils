#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
from celery import Celery, platforms
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s: %(levelname)s [%(name)s:%(funcName)s] %(message)s')
logger = logging.getLogger()
# brokers = 'redis://127.0.0.1:6379/5'
# backend = 'redis://127.0.0.1:6379/6'

app = Celery('tasks')  # , broker=brokers, backend=backend
app.config_from_object('celeryconfig')
platforms.C_FORCE_ROOT = True

# celery -A tasks2 worker  --loglevel=info

@app.task
def add(x, y):
    logger.info('%d + %d runing', x, y)
    ret = x + y
    time.sleep(ret)
    logger.info('%d + %d = %d task finished', x, y, ret)
    return ret