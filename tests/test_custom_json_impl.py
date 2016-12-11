from __future__ import unicode_literals
import unittest
from jsontraverse.parser import JsonTraverseParser

class CustomJsonImpl:
    return_value = "custom_json_impl"

    @staticmethod
    def loads(*args):
        return CustomJsonImpl.return_value

class JsonTraverseParserTest(unittest.TestCase):
    def test_empty_data_still_none(self):
        parser = JsonTraverseParser('', custom_json_impl=CustomJsonImpl)
        self.assertEqual(parser.data, None)

    def test_simple_data_uses_custom_impl(self):
        parser = JsonTraverseParser('{"a": 0}', custom_json_impl=CustomJsonImpl)
        self.assertEqual(parser.data, CustomJsonImpl.return_value)
