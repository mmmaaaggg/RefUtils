#!/usr/bin/env python
# -*- coding:utf-8 -*-

from celery import Celery, platforms

app = Celery('tasks', include=['celeryproj.tasks'])
platforms.C_FORCE_ROOT = True
app.config_from_object('celeryproj.config')

if __name__ == '__main__':
    app.start()
