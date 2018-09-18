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
import json
import bitmex
client = bitmex.bitmex()
# client = bitmex.bitmex(api_key='AEwP_4JmXWyFff5KP2-5OUkp', api_secret='DRyB920Sqb9LOgZXX3xowTEezJVBMc-zqrLVz4xOIqwAw4tf')
# testnet
# apiKey = 'AEwP_4JmXWyFff5KP2-5OUkp'
# apiSecret = 'DRyB920Sqb9LOgZXX3xowTEezJVBMc-zqrLVz4xOIqwAw4tf'
# client = bitmex.bitmex(test=False, api_key=apiKey, api_secret=apiSecret)
# result = client.Quote.Quote_get(symbol='XBTUSD').result()
# result = client.Quote.Quote_get(symbol="XBTUSD", reverse=True, count=1).result()
# 403 Forbidden

# apiKey = 'avEW3othNxCmXIUtrRo2BeRg'
# apiSecret = 'APkFrY-SNOimhCXXs4MGaJLgo27koculwNRRSw1XWTOkenjt'
# client = bitmex.bitmex(test=False, api_key=apiKey, api_secret=apiSecret)
# result = client.Quote.Quote_get(symbol='XBTUSD').result()
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
#   File "/home/mg/wspy/venv/lib/python3.6/site-packages/bravado/http_future.py", line 213, in result
#     swagger_result = self._get_swagger_result(incoming_response)
#   File "/home/mg/wspy/venv/lib/python3.6/site-packages/bravado/http_future.py", line 237, in _get_swagger_result
#     self.request_config.response_callbacks,
#   File "/home/mg/wspy/venv/lib/python3.6/site-packages/bravado/http_future.py", line 282, in unmarshal_response
#     raise_on_expected(incoming_response)
#   File "/home/mg/wspy/venv/lib/python3.6/site-packages/bravado/http_future.py", line 342, in raise_on_expected
#     swagger_result=http_response.swagger_result)
# bravado.exception.HTTPForbidden: 403 Forbidden: <html>
# <head><title>403 Forbidden</title></head>
# <body bgcolor="white">
# <center><h1>403 Forbidden</h1></center>
# </body>
# </html>

apiKey = 'K5DaKlClbXg_TQn5lEGOswd8'
apiSecret = 'QQwPpUpCUcJwtqFIsDXevMqhEPUM3eanZUnzlSpYGqaLIbph'
client = bitmex.bitmex(api_key=apiKey, api_secret=apiSecret)
client.Position.Position_get(filter=json.dumps({'symbol': 'XBTUSD'})).result()


client = bitmex.bitmex()
client.Instrument.Instrument_get(filter=json.dumps({'symbol': 'XBTJPY'})).result()
