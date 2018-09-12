#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/9/4 13:42
@File    : bitmax_connector_api_test.py.py
@contact : mmmaaaggg@163.com
@desc    :
https://github.com/BitMEX/api-connectors/tree/master/auto-generated/python
python setup.py install
"""

from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: apiKey
configuration = swagger_client.Configuration()
configuration.api_key['api-key'] = 'DRyB920Sqb9LOgZXX3xowTEezJVBMc-zqrLVz4xOIqwAw4tf'
configuration.host = "https://testnet.bitmex.com/api/v1"
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['api-key'] = 'Bearer'
# Configure API key authorization: apiNonce
configuration = swagger_client.Configuration()
configuration.api_key['api-nonce'] = 'DRyB920Sqb9LOgZXX3xowTEezJVBMc-zqrLVz4xOIqwAw4tf'
configuration.host = "https://www.bitmex.com/api/v1"
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['api-nonce'] = 'Bearer'
# Configure API key authorization: apiSignature
configuration = swagger_client.Configuration()
configuration.api_key['api-signature'] = 'DRyB920Sqb9LOgZXX3xowTEezJVBMc-zqrLVz4xOIqwAw4tf'
configuration.host = "https://www.bitmex.com/api/v1"
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['api-signature'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.APIKeyApi(swagger_client.ApiClient(configuration))
api_key_id = 'AEwP_4JmXWyFff5KP2-5OUkp' # str | API Key ID (public component).

try:
    # Disable an API Key.
    # api_response = api_instance.a_pi_key_enable(api_key_id)
    # pprint(api_response)
    char = swagger_client.ChatApi(swagger_client.ApiClient(configuration))
    json = char.chat_get()
except ApiException as e:
    print("Exception when calling APIKeyApi->a_pi_key_disable: %s\n" % e)
