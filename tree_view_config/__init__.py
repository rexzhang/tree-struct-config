#!/usr/bin/env python
# coding=utf-8


"""
Tree View Config - A configuration module for python, support dump from/to JSON.
"""

from .core import (  # noqa: F401
    IntLeaf,
    StringLeaf,
    BooleanLeaf,

    BranchNode,
    RootNode,
)

__version__ = '0.1.0'

__author__ = 'Rex Zhang'
__author_email__ = 'rex.zhang@gmail.com'
__licence__ = 'MIT'

__description__ = 'A configuration module for python, support dump to/from JSON'
__project_url__ = 'https://github.com/rexzhang/tree-view-config'
