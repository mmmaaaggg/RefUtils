#!/usr/bin/env python
# -*- coding:utf-8 -*-
from datetime import timedelta
from celery.schedules import crontab

CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/5'
BROKER_URL = 'redis://127.0.0.1:6379/6'

CELERY_TIMEZONE = 'Asia/Shanghai'


CELERYBEAT_SCHEDULE = {
    'add-every-30-seconds': {
        'task': 'celeryproj.tasks.add',
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
