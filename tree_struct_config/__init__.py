#!/usr/bin/env python
# coding=utf-8


"""
Tree Struct Config - A Tree Struct Configuration module for python, support dump from/to JSON.
"""

from .core import (  # noqa: F401
    IntLeaf,
    StringLeaf,
    BooleanLeaf,

    BranchNode,
    RootNode,

    ConfigDecodeError,
)

__version__ = '0.1.0'

__author__ = 'Rex Zhang'
__author_email__ = 'rex.zhang@gmail.com'
__licence__ = 'MIT'

__description__ = 'Tree Struct Config - A Tree Struct Configuration module for python, support dump from/to JSON'
__project_url__ = 'https://github.com/rexzhang/tree-struct-config'
