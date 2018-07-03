#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import unittest
from unittest import mock
import sys, os
# lib_path = os.path.abspath('.')
# sys.path.append(lib_path)
# import client
from src.fh_tools.language_test.mock_test import client


class TestClient(unittest.TestCase):
    def test_success_request(self):
        success_send = mock.Mock(return_value='200')
        client.send_request = success_send
        self.assertEqual(client.visit_ustack(), '200')

    def test_fail_request(self):
        fail_send = mock.Mock(return_value='404')
        client.send_request = fail_send
        self.assertEqual(client.visit_ustack(), '404')


class TestClient2(unittest.TestCase):

    def test_success_request(self):
        status_code = '200'
        success_send = mock.Mock(return_value=status_code)
        with mock.patch('src.fh_tools.language_test.mock_test.client.send_request', success_send):
            from src.fh_tools.language_test.mock_test.client import visit_ustack
            # from ..mock_test.client import visit_ustack
            self.assertEqual(visit_ustack(), status_code)

    def test_fail_request1(self):
        status_code = '404'
        fail_send = mock.Mock(return_value=status_code)
        with mock.patch('src.fh_tools.language_test.mock_test.client.send_request', fail_send):
            from src.fh_tools.language_test.mock_test.client import visit_ustack
            self.assertEqual(visit_ustack(), status_code)

    def test_call_foo(self):
        ret_1 = mock.Mock(return_value=6)
        classfoo = client.ClassFoo()
        with mock.patch.object(classfoo, 'invoke', ret_1):
            self.assertEqual(classfoo.foo(2, 3), 6)

    def test_fail_request2(self):
        status_code = '404'
        fail_send = mock.Mock(return_value=status_code)
        with mock.patch.object(client, 'send_request', fail_send):
            from src.fh_tools.language_test.mock_test.client import visit_ustack
            self.assertEqual(visit_ustack(), status_code)

if __name__ == '__main__':
    unittest.main()
