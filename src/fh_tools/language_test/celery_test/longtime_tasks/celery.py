#!/usr/bin/env python
# -*- coding:utf-8 -*-

from celery import Celery, platforms

app = Celery('longtime_tasks', include=['longtime_tasks.tasks'])
platforms.C_FORCE_ROOT = True
app.config_from_object('longtime_tasks.config')

if __name__ == '__main__':
    # celery -A longtime_tasks worker -B -l info
    app.start()
