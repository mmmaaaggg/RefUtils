"""
@author  : MG
@Time    : 2021/3/10 8:03
@File    : mock_side_effect.py
@contact : mmmaaaggg@163.com
@desc    : 用于
"""
import unittest
from unittest import mock, TestCase
from functools import partial
from src.fh_tools.language_test.mock_test.side_effect_on_object_method.foo_cls import HelloFoo


def mock_func(_self: HelloFoo, sth):
    words = f"[mock]{_self.name}: {sth}"
    print(words)
    return words


class TestClient2(TestCase):

    def test_side_effect(self):
        name = 'Me'
        foo = HelloFoo(name)
        side_effect = mock.Mock(side_effect=partial(mock_func, foo))
        with mock.patch.object(HelloFoo, 'say', side_effect):
            sth = 'hello'
            words = foo.say(sth)
            self.assertEqual(words, f"[mock]{name}: {sth}")


if __name__ == "__main__":
    unittest.main()
