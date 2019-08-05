#!/usr/bin/env python
# coding=utf-8


"""
Tree Struct Config
"""

from .core import (  # noqa: F401
    IntLeaf,
    StringLeaf,
    BooleanLeaf,
    ListLeaf,

    BranchNode,

    RootNode,
    SerializationFormat,
    SerializationDecodeError,
)

__version__ = '0.1.0'

__author__ = 'Rex Zhang'
__author_email__ = 'rex.zhang@gmail.com'
__licence__ = 'MIT'

__description__ = 'A Tree Struct Configuration module for python, support dump to/from JSON'
__project_url__ = 'https://github.com/rexzhang/tree-struct-config'
