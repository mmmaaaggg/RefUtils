#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/4/8 13:39
@File    : flask_db.py
@contact : mmmaaaggg@163.com
@desc    : 
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src.fh_tools.language_test.flask_test.config import ConfigClass

app = Flask(__name__, static_url_path='')
db = SQLAlchemy()

db.init_app(app)
