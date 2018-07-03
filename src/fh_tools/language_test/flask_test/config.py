#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/3/30 17:53
@File    : config.py
@contact : mmmaaaggg@163.com
@desc    : 
"""
import os
import logging
from logging.config import dictConfig


# Use a Class-based config to avoid needing a 2nd file
# os.getenv() enables configuration through OS environment variables
class ConfigClass(object):
    # Flask settings
    SECRET_KEY =              os.getenv('SECRET_KEY',       'THIS IS AN INSECURE SECRET')
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',     'sqlite:///basic1_app.sqlite')
    SQLALCHEMY_DATABASE_URI = 'mysql://mg:Abcd1234@localhost/prophet'
    CSRF_ENABLED = True

    # Flask-Mail settings
    USER_SEND_PASSWORD_CHANGED_EMAIL = False
    USER_SEND_REGISTERED_EMAIL = False
    USER_SEND_USERNAME_CHANGED_EMAIL = False
    MAIL_USERNAME =           os.getenv('MAIL_USERNAME',        '265590706@qq.com')
    MAIL_PASSWORD =           os.getenv('MAIL_PASSWORD',        'mduwrytdphgxbgij')
    MAIL_DEFAULT_SENDER =     os.getenv('MAIL_DEFAULT_SENDER',  '"MyApp" <265590706@qq.com>')
    MAIL_SERVER =             os.getenv('MAIL_SERVER',          'smtp.qq.com')
    MAIL_PORT =           int(os.getenv('MAIL_PORT',            '465'))
    MAIL_USE_SSL =        int(os.getenv('MAIL_USE_SSL',         True))

    # Flask-User settings
    USER_APP_NAME        = "AppName"                # Used by email templates

    # log settings
    logging_config = dict(
        version=1,
        formatters={
            'simple': {
                'format': '%(levelname)s %(asctime)s { Module : %(module)s Line No : %(lineno)d} %(message)s'}
        },
        handlers={
            'file_handler': {'class': 'logging.handlers.RotatingFileHandler',
                  'filename': 'logger.log',
                  'maxBytes': 1024 * 1024 * 10,
                  'backupCount': 5,
                  'level': 'DEBUG',
                  'formatter': 'simple',
                  'encoding': 'utf8'},
            'console_handler':{'class':'logging.StreamHandler',
                               'level':'DEBUG',
                               'formatter':'simple'}
        },

        root={
            'handlers': ['console_handler','file_handler'],
            'level': logging.DEBUG,
        }
    )
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARN)
    dictConfig(logging_config)