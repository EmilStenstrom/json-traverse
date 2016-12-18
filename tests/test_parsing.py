from __future__ import unicode_literals
import json
import unittest
from jsontraverse.parser import JsonTraverseParser

str = "".__class__

class JsonTraverseParserTest(unittest.TestCase):
    def test_empty_data(self):
        parser = JsonTraverseParser('')
        self.assertEqual(parser.traverse(''), None)
        self.assertEqual(parser.traverse('', force_list=True), [])

    def test_empty_data_invalid(self):
        parser = JsonTraverseParser('')
        self.assertEqual(parser.traverse('0'), None)
        self.assertEqual(parser.traverse('1'), None)
        self.assertEqual(parser.traverse('a'), None)
        self.assertEqual(parser.traverse('a', force_list=True), [])

    def test_list_data(self):
        parser = JsonTraverseParser('[1]')
        self.assertEqual(parser.traverse(''), [1])
        self.assertEqual(parser.traverse('', force_list=True), [1])
        self.assertEqual(parser.traverse('0'), 1)
        self.assertEqual(parser.traverse('0', force_list=True), [1])

    def test_list_data_invalid(self):
        parser = JsonTraverseParser('[1]')
        self.assertEqual(parser.traverse('a'), None)
        self.assertEqual(parser.traverse('a.0'), None)
        self.assertEqual(parser.traverse('1'), None)
        self.assertEqual(parser.traverse('1.a'), None)
        self.assertEqual(parser.traverse('0.a'), None)
        self.assertEqual(parser.traverse('0.a', force_list=True), [])

    def test_dict_data(self):
        parser = JsonTraverseParser('{"a": 1}')
        self.assertEqual(parser.traverse(''), {"a": 1})
        self.assertEqual(parser.traverse('', force_list=True), [{"a": 1}])
        self.assertEqual(parser.traverse('a'), 1)
        self.assertEqual(parser.traverse('a', force_list=True), [1])

    def test_dict_data_invalid(self):
        parser = JsonTraverseParser('{"a": 1}')
        self.assertEqual(parser.traverse('0'), None)
        self.assertEqual(parser.traverse('b'), None)
        self.assertEqual(parser.traverse('a.a'), None)
        self.assertEqual(parser.traverse('a.0'), None)
        self.assertEqual(parser.traverse('a.0', force_list=True), [])

    def test_dict_list_data(self):
        parser = JsonTraverseParser('{"a": [0, 1]}')
        self.assertEqual(parser.traverse('a'), [0, 1])
        self.assertEqual(parser.traverse('a', force_list=True), [0, 1])
        self.assertEqual(parser.traverse('a.0'), 0)
        self.assertEqual(parser.traverse('a.0', force_list=True), [0])
        self.assertEqual(parser.traverse('a.1'), 1)
        self.assertEqual(parser.traverse('a.1', force_list=True), [1])

    def test_dict_list_data_invalid(self):
        parser = JsonTraverseParser('{"a": [0, 1]}')
        self.assertEqual(parser.traverse('b'), None)
        self.assertEqual(parser.traverse('b.0'), None)
        self.assertEqual(parser.traverse('0'), None)
        self.assertEqual(parser.traverse('a.2'), None)
        self.assertEqual(parser.traverse('a.2', force_list=True), [])

    def test_list_dict_data(self):
        parser = JsonTraverseParser('[{"a": 0}, {"b": 1}]')
        self.assertEqual(parser.traverse('0'), {"a": 0})
        self.assertEqual(parser.traverse('0', force_list=True), [{"a": 0}])
        self.assertEqual(parser.traverse('0.a'), 0)
        self.assertEqual(parser.traverse('0.a', force_list=True), [0])
        self.assertEqual(parser.traverse('1'), {"b": 1})
        self.assertEqual(parser.traverse('1', force_list=True), [{"b": 1}])
        self.assertEqual(parser.traverse('1.b'), 1)
        self.assertEqual(parser.traverse('1.b', force_list=True), [1])
        self.assertEqual(parser.traverse('a'), 0)
        self.assertEqual(parser.traverse('a', force_list=True), [0])

    def test_list_dict_data_invalid(self):
        parser = JsonTraverseParser('[{"a": 0}, {"b": 1}]')
        self.assertEqual(parser.traverse('a.0'), None)
        self.assertEqual(parser.traverse('2'), None)
        self.assertEqual(parser.traverse('2', force_list=True), [])

    def test_string_data(self):
        parser = JsonTraverseParser('"hello world"')
        self.assertEqual(parser.traverse(''), "hello world")
        self.assertEqual(parser.traverse('', force_list=True), ["hello world"])

        parser = JsonTraverseParser('{"hello world": ["hello", "world"]}')
        self.assertEqual(parser.traverse('hello world.0'), "hello")
        self.assertEqual(parser.traverse('hello world.0', force_list=True), ["hello"])
        self.assertEqual(parser.traverse('hello world.0.0'), "h")
        self.assertEqual(parser.traverse('hello world.0.0', force_list=True), ["h"])

    def test_null(self):
        parser = JsonTraverseParser('')
        with self.assertRaises(TypeError):
            parser.traverse(None)

        parser = JsonTraverseParser(None)
        self.assertEqual(parser.traverse(''), None)
        with self.assertRaises(TypeError):
            parser.traverse(None)

    def test_bytes(self):
        with self.assertRaises(TypeError):
            parser = JsonTraverseParser(b'[]')

        parser = JsonTraverseParser('')
        with self.assertRaises(TypeError):
            parser.traverse(b'a')

    def test_multi_character_keys(self):
        # [0, 1, 2, ... 99]
        parser = JsonTraverseParser(str(json.dumps(list(range(0, 100)))))
        self.assertEqual(parser.traverse('99'), 99)
        self.assertEqual(parser.traverse('99', force_list=True), [99])

        # {"a": 0, "aa": 1, "aaa": 2, ... "aaaa...": 99}
        parser = JsonTraverseParser(str(json.dumps({"a" * i: i for i in range(0, 100)})))
        self.assertEqual(parser.traverse('a' * 99), 99)
        self.assertEqual(parser.traverse('a' * 99, force_list=True), [99])

    def test_multiple_return_values(self):
        parser = JsonTraverseParser('{"a": [{"b": [{"c": 0}, {"c": 1}]}, {"b": [{"c": 2}, {"c": 3}]}]}')
        self.assertEqual(parser.traverse('a.b.c'), [0, 1, 2, 3])
        self.assertEqual(parser.traverse('a.b.c', force_list=True), [0, 1, 2, 3])

        parser = JsonTraverseParser('{"a": [{"b": {"c": 0}}, {"b": [{"c": 1}, {"c": 2}]}]}')
        self.assertEqual(parser.traverse('a.b.c'), [0, 1, 2])
        self.assertEqual(parser.traverse('a.b.c', force_list=True), [0, 1, 2])

        parser = JsonTraverseParser('[{"a": 0}, {"a": {"b": 1}}]')
        self.assertEqual(parser.traverse('a.b'), 1)
        self.assertEqual(parser.traverse('a.b', force_list=True), [1])

    def test_string_and_digit_keys_invalid(self):
        parser = JsonTraverseParser('[{"a": 0}]')
        self.assertEqual(parser.traverse('a0.0'), None)
        self.assertEqual(parser.traverse('0a.a'), None)
        self.assertEqual(parser.traverse('0.a0'), None)
        self.assertEqual(parser.traverse('0.0a'), None)
        self.assertEqual(parser.traverse('A'), None)

    def test_unstandard_digit_keys_invalid(self):
        parser = JsonTraverseParser('[{"a": 0}]')
        self.assertEqual(parser.traverse('00.0'), None)
        self.assertEqual(parser.traverse('01.0'), None)
        self.assertEqual(parser.traverse('0001.0'), None)
        self.assertEqual(parser.traverse('-1.0'), None)

    def test_digit_keys_in_dict(self):
        parser = JsonTraverseParser('[{"0": 0}]')
        self.assertEqual(parser.traverse('0.0'), 0)
        self.assertEqual(parser.traverse('0.0', force_list=True), [0])
