from __future__ import unicode_literals
import json
import unittest
from jsontraverse.parser import JsonMultiParser

str = "".__class__

class JsonMultiParserTest(unittest.TestCase):
    def test_empty_data(self):
        parser = JsonMultiParser('')
        self.assertEqual(parser.traverse(''), '')

    def test_empty_data_invalid(self):
        parser = JsonMultiParser('')
        self.assertEqual(parser.traverse('0'), '')
        self.assertEqual(parser.traverse('1'), '')
        self.assertEqual(parser.traverse('a'), '')

    def test_list_data(self):
        parser = JsonMultiParser('[1]')
        self.assertEqual(parser.traverse(''), [1])
        self.assertEqual(parser.traverse('0'), 1)

    def test_list_data_invalid(self):
        parser = JsonMultiParser('[1]')
        self.assertEqual(parser.traverse('a'), [1])
        self.assertEqual(parser.traverse('a.0'), [1])
        self.assertEqual(parser.traverse('1'), [1])
        self.assertEqual(parser.traverse('1.a'), [1])
        self.assertEqual(parser.traverse('0'), 1)
        self.assertEqual(parser.traverse('0.a'), 1)

    def test_dict_data(self):
        parser = JsonMultiParser('{"a": 1}')
        self.assertEqual(parser.traverse(''), {"a": 1})
        self.assertEqual(parser.traverse('a'), 1)

    def test_dict_data_invalid(self):
        parser = JsonMultiParser('{"a": 1}')
        self.assertEqual(parser.traverse('0'), {"a": 1})
        self.assertEqual(parser.traverse('b'), {"a": 1})
        self.assertEqual(parser.traverse('a.a'), 1)
        self.assertEqual(parser.traverse('a.0'), 1)

    def test_dict_list_data(self):
        parser = JsonMultiParser('{"a": [0, 1]}')
        self.assertEqual(parser.traverse('a'), [0, 1])
        self.assertEqual(parser.traverse('a.0'), 0)
        self.assertEqual(parser.traverse('a.1'), 1)

    def test_dict_list_data_invalid(self):
        parser = JsonMultiParser('{"a": [0, 1]}')
        self.assertEqual(parser.traverse('b'), {"a": [0, 1]})
        self.assertEqual(parser.traverse('b.0'), {"a": [0, 1]})
        self.assertEqual(parser.traverse('0'), {"a": [0, 1]})
        self.assertEqual(parser.traverse('a.2'), [0, 1])

    def test_list_dict_data(self):
        parser = JsonMultiParser('[{"a": 0}, {"b": 1}]')
        self.assertEqual(parser.traverse('0'), {"a": 0})
        self.assertEqual(parser.traverse('0.a'), 0)
        self.assertEqual(parser.traverse('1'), {"b": 1})
        self.assertEqual(parser.traverse('1.b'), 1)

    def test_list_dict_data_invalid(self):
        parser = JsonMultiParser('[{"a": 0}, {"b": 1}]')
        self.assertEqual(parser.traverse('a'), [0, {"b": 1}])
        self.assertEqual(parser.traverse('a.0'), [0, {"b": 1}])
        self.assertEqual(parser.traverse('2'), [{"a": 0}, {"b": 1}])

    def test_string_data(self):
        parser = JsonMultiParser('"hello world"')
        self.assertEqual(parser.traverse(''), "hello world")

        parser = JsonMultiParser('{"hello world": ["hello", "world"]}')
        self.assertEqual(parser.traverse('hello world.0'), "hello")
        self.assertEqual(parser.traverse('hello world.0.0'), "h")

    def test_null(self):
        parser = JsonMultiParser('')
        with self.assertRaises(TypeError):
            parser.traverse(None)

        parser = JsonMultiParser(None)
        self.assertEqual(parser.traverse(''), '')
        with self.assertRaises(TypeError):
            parser.traverse(None)

    def test_bytes(self):
        with self.assertRaises(TypeError):
            parser = JsonMultiParser(b'[]')

        parser = JsonMultiParser('')
        with self.assertRaises(TypeError):
            parser.traverse(b'a')

    def test_multi_character_keys(self):
        # [0, 1, 2, ... 99]
        parser = JsonMultiParser(str(json.dumps(list(range(0, 100)))))
        self.assertEqual(parser.traverse('99'), 99)

        # {"a": 0, "aa": 1, "aaa": 2, ... "aaaa...": 99}
        parser = JsonMultiParser(str(json.dumps({"a" * i: i for i in range(0, 100)})))
        self.assertEqual(parser.traverse('a' * 99), 99)

    def test_multiple_return_values(self):
        parser = JsonMultiParser('{"a": [{"b": [{"c": 0}, {"c": 1}]}, {"b": [{"c": 2}, {"c": 3}]}]}')
        self.assertEqual(parser.traverse('a.b.c'), [0, 1, 2, 3])

        parser = JsonMultiParser('{"a": [{"b": {"c": 0}}, {"b": [{"c": 1}, {"c": 2}]}]}')
        self.assertEqual(parser.traverse('a.b.c'), [0, 1, 2])

        parser = JsonMultiParser('[{"a": 0}, {"a": {"b": 1}}]')
        self.assertEqual(parser.traverse('a.b'), [0, 1])

    def test_string_and_digit_keys_invalid(self):
        parser = JsonMultiParser('[{"a": 0}]')
        self.assertEqual(parser.traverse('a0.0'), [{"a": 0}])
        self.assertEqual(parser.traverse('0a.a'), [{"a": 0}])
        self.assertEqual(parser.traverse('0.a0'), {"a": 0})
        self.assertEqual(parser.traverse('0.0a'), {"a": 0})
        self.assertEqual(parser.traverse('A'), [{"a": 0}])

    def test_unstandard_digit_keys_invalid(self):
        parser = JsonMultiParser('[{"a": 0}]')
        self.assertEqual(parser.traverse('00.0'), [{"a": 0}])
        self.assertEqual(parser.traverse('01.0'), [{"a": 0}])
        self.assertEqual(parser.traverse('0001.0'), [{"a": 0}])
        self.assertEqual(parser.traverse('-1.0'), [{"a": 0}])

    def test_digit_keys_in_dict(self):
        parser = JsonMultiParser('[{"0": 0}]')
        self.assertEqual(parser.traverse('0.0'), 0)
