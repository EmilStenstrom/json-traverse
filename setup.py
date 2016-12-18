# -*- coding: utf-8 -*-
from setuptools import setup

VERSION = '0.4'
PKG_NAME = 'json-traverse'

setup(
    name=PKG_NAME,
    packages=[PKG_NAME.replace("-", "")],
    version=VERSION,
    description='Query complex JSON structures using a simple query syntax.',
    author=u'Emil Stenström',
    author_email='em@kth.se',
    url='https://github.com/EmilStenstrom/{}/'.format(PKG_NAME),
    download_url='https://github.com/EmilStenstrom/{}/archive/{}.zip'.format(PKG_NAME, VERSION),
    install_requires=[],
    keywords=['json', 'query', 'tree', 'parser', 'json-query'],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
    ],
)
