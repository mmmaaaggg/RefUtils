#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/4/1 10:49
@File    : wtf_test.py
@contact : mmmaaaggg@163.com
@desc    : 
"""

from flask import Flask, render_template
from flask_wtf import Form
import wtforms

app = Flask(__name__, static_url_path='')
app.debug = True
app.secret_key = 'M!@#$@#$%#$%alksdjf;lkj'

@app.route("/")
def hello_world():
    form = test_form()

    return render_template('hello_world.html', form=form)


class test_form(Form):
    name = wtforms.StringField('名字')
    gender = wtforms.StringField('性别')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)