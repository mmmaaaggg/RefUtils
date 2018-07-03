#!/usr/bin/env python
# -*- coding:utf-8 -*-
from datetime import timedelta
from celery.schedules import crontab

REDIS_HOST, REDIS_PORT, REDIS_DB_OTHER = '127.0.0.1', '6379', 7
CELERY_RESULT_BACKEND = 'redis://%(REDIS_HOST)s:%(REDIS_PORT)s/5' % {'REDIS_HOST': REDIS_HOST, 'REDIS_PORT': REDIS_PORT}
BROKER_URL = 'redis://%(REDIS_HOST)s:%(REDIS_PORT)s/6' % {'REDIS_HOST': REDIS_HOST, 'REDIS_PORT': REDIS_PORT}


CELERY_TIMEZONE = 'Asia/Shanghai'


CELERYBEAT_SCHEDULE = {
    'add-every-30-seconds': {
        'task': 'longtime_tasks.tasks.add',
        'schedule': timedelta(seconds=30),
        'args': (16, 16)
    },
}

# CELERYBEAT_SCHEDULE = {
#     # Executes every Monday morning at 7:30 A.M
#     'add-every-monday-morning': {
#         'task': 'tasks.add',
#         'schedule': crontab(hour=7, minute=30, day_of_week=1),
#         'args': (16, 16),
#     },
# }
