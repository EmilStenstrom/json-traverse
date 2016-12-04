# json-traverse
Query complex JSON structures using a simple query syntax.

## Why should you use json-traverse?

- It makes parsing JSON easy and compact
- The code is simple, only ~100 lines of code
- It works with both Python 2 and Python 3
- It includes a comprehensive unit test suite
- It has no dependencies

## Installation

```bash
pip install json-traverse
```

## Usage

Let's say we've fetched some data and stored it in a variable called `json_data`. All lines that start with ">>> " are things that you type. All other lines are output from json-traverse. Follow along by starting your terminal and typing 'python'.

```python
>>> from __future__ import unicode_literals  # Only needed for Python 2
>>> from jsontraverse.parser import JsonTraverseParser

>>> # We'll use the example JSON from [http://json.org/example.html]
>>> json_data = """
{
  "menu": {
    "id": "file",
    "value": "File",
    "popup": {
      "menuitem": [
        {"value": "New", "onclick": "CreateNewDoc()"},
        {"value": "Open", "onclick": "OpenDoc()"},
        {"value": "Close", "onclick": "CloseDoc()"}
      ]
    }
  }
}
"""

>>> # Create a JsonTraverseParser. We do this once and can then parse
>>> # the same data multiple times.
>>> parser = JsonTraverseParser(json_data)

>>> # Now we're ready to type our first query against the structure above.

>>> # Let's start by getting the value of the menu:
>>> parser.traverse("menu.value")
'File'

>>> # Easy right? Now lets get all the values from all menu items:
>>> parser.traverse("menu.popup.menuitem.value")
['New', 'Open', 'Close']

>>> # Only the first menuitem?
>>> parser.traverse("menu.popup.menuitem.0.value")
'New'
```

See the [tests](tests/test_parsing.py) for more examples.

## How does it all work? How exactly does the algoritm work?

1. You send in a query in the form of a string with parts separated by a period (.).
2. Json-traverse splits that path into several items and tries to search through the json data step by step, each step reducing the data to a smaller set.
3. Each item in the path is first checked to see if it's an array index. If it is, the data is treated as a list and only the data matching the index is returned.
4. If it's not an index, it's treated as a dict key instead. The data is treated as an dict and only the data inside the specified key is returned.
5. If you specified a dict key, but the data is a list, the result is split into as many parts as there are items in the list, and the key is searched for in each part.
6. If at any time an invalid item is tried, searching stops and the result so far is returned.

See the [parser code](jsontraverse/parser.py) for more details.

## Interested in helping out?

I's love to see suggestions on how this library can be better. It's still early, and I'm open to changing things based on your feedback.

## Develop locally and run the tests

```bash
git clone git@github.com:EmilStenstrom/json-traverse.git
cd json-traverse
```

Install `tox`:

```sh
pip install tox
```

Then run all the tests over all Python versions (Make sure you have python2.7, python3.3, python3.4, and python3.5 on your PATH first):

```sh
tox
```

Or just the particular version you wish to test:

```sh
tox -e py35
```

You can also have it watch the directory for changes and re-run the tests:

```sh
tox -e py35 -- -f
```
