#!/usr/bin/env python
# -*- coding:utf-8 -*-

from datetime import timedelta
import logging

logger = logging.getLogger()
logger.info('celeryconfig loaded ')
print('celeryconfig loaded ')

BROKER_URL = 'redis://127.0.0.1:6379/5'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/6'
CELERYBEAT_SCHEDULE = {
    'add-every-30-seconds': {
        'task': 'tasks2.add',
        'schedule': timedelta(seconds=5),
        'args': (16, 16),
    },
}

CELERY_TIMEZONE = 'Asia/Shanghai'
