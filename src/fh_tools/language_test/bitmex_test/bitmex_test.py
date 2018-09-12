#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/9/4 9:55
@File    : bitmex_test.py
@contact : mmmaaaggg@163.com
@desc    : https://github.com/BitMEX/api-connectors/tree/master/official-http/python-swaggerpy
from Official Examples Python-SwaggerPy
"""

import bitmex
client = bitmex.bitmex()
# client = bitmex.bitmex(api_key='AEwP_4JmXWyFff5KP2-5OUkp', api_secret='DRyB920Sqb9LOgZXX3xowTEezJVBMc-zqrLVz4xOIqwAw4tf')
# testnet
apiKey = 'avEW3othNxCmXIUtrRo2BeRg'
apiSecret = 'APkFrY-SNOimhCXXs4MGaJLgo27koculwNRRSw1XWTOkenjt'
client = bitmex.bitmex(api_key=apiKey, api_secret=apiSecret)
result = client.Quote.Quote_get(symbol='XBTUSD').result()
result = client.Quote.Quote_get(symbol="XBTUSD", reverse=True, count=1).result()

HMAC_SHA256