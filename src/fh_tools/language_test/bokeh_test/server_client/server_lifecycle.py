#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/3/2 14:51
@File    : server_lifecycle.py
@contact : mmmaaaggg@163.com
@desc    : 
"""

def on_server_loaded(server_context):
    ''' If present, this function is called when the server first starts. '''
    print("server loaded")

def on_server_unloaded(server_context):
    ''' If present, this function is called when the server shuts down. '''
    print("server unloaded")


def on_session_created(session_context):
    ''' If present, this function is called when a session is created. '''
    print("session created")

def on_session_destroyed(session_context):
    ''' If present, this function is called when a session is closed. '''
    print("session destroyed")
