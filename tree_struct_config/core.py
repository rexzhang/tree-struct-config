#!/usr/bin/env python
# coding=utf-8


import json
from enum import Enum
from json import JSONDecodeError

ROOT_NODE_FUNC_NAME_SET = {'dump', 'dumps', 'load', 'loads'}


class SerializationFormat(Enum):
    JSON = 1
    TOML = 2


class SerializationDecodeError(ValueError):
    pass


class NodeType(Enum):
    NONE = 0
    LEAF = 2
    BRANCH = 1
    ROOT = 3


class NodeBase(object):
    _node_type = NodeType.NONE

    # def __setattr__(self, key, value):
    #     print('>>>', key, value)
    #     super().__setattr__(key, value)


class LeafNodeMetaClass(type):
    pass


class BranchNodeMetaClass(type):
    pass


class RootNodeMetaClass(type):
    pass


class LeafNode(NodeBase, metaclass=LeafNodeMetaClass):
    _node_type = NodeType.LEAF

    _value = None
    _default_value = None

    def __init__(self, default=None):
        if default is None:
            self._value = self._default_value

        else:
            self._value = default

    def __get__(self, instance, owner):
        # print('<<< get', instance, owner)
        return self._value

    def __set__(self, instance, value):
        # print('>>> set', instance, value)
        # TODO: can't run to here at multi-nested mode, maybe python VM's bug
        self._value = value

    # def __delete__(self, instance):
    #     print('!!! delete')
    #
    # def __setattr__(self, key, value):
    #     print('>>>', key, value)
    #     super().__setattr__(key, value)


class IntLeaf(LeafNode):
    _default_value = 0


class StringLeaf(LeafNode):
    _default_value = ''


class BooleanLeaf(LeafNode):
    _default_value = False


class ListLeaf(LeafNode):
    _default_value = list()


class BranchNode(NodeBase, metaclass=BranchNodeMetaClass):
    _node_type = NodeType.BRANCH


def tree_struct2obj(cls, is_root_node=False):
    obj = {}

    for child_node_name in dir(cls):
        if child_node_name[0] == '_':
            continue

        if is_root_node and child_node_name in ROOT_NODE_FUNC_NAME_SET:
            continue

        child_node = getattr(cls, child_node_name)

        if type(child_node) == type(BranchNode):
            # NodeType.BRANCH
            obj[child_node_name] = tree_struct2obj(child_node)

        # elif type(child_node) == type(RootNode):
        #     # NodeType.ROOT
        #     # raise('!!!!')
        #     print('!!!!!!')
        #     continue

        else:
            # NodeType.LEAF
            obj[child_node_name] = child_node

    return obj


def obj2tree_struct(cls, obj, is_root_node=False):
    for child_node_name in dir(cls):
        if child_node_name[0] == '_':
            continue

        if is_root_node and child_node_name in ROOT_NODE_FUNC_NAME_SET:
            continue

        child_node = getattr(cls, child_node_name)

        if type(child_node) == type(BranchNode):
            # NodeType.BRANCH
            obj2tree_struct(child_node, obj[child_node_name])

        else:
            # NodeType.LEAF
            if child_node_name not in obj:
                continue

            setattr(cls, child_node_name, obj[child_node_name])

    return


class RootNode(NodeBase, metaclass=RootNodeMetaClass):
    _node_type = NodeType.ROOT
    _serialization_format = SerializationFormat.JSON

    def __init__(self, serialization_format=SerializationFormat.JSON):
        if isinstance(serialization_format, SerializationFormat):
            self._serialization_format = serialization_format

    def dumps(self, serialization_format=None):
        if isinstance(serialization_format, SerializationFormat):
            self._serialization_format = serialization_format

        obj = tree_struct2obj(self, is_root_node=True)

        if self._serialization_format == SerializationFormat.TOML:
            import toml

            s = toml.dumps(obj)

        else:
            s = json.dumps(obj, indent=2)

        return s

    def loads(self, s, serialization_format=None):
        if isinstance(serialization_format, SerializationFormat):
            self._serialization_format = serialization_format

        if self._serialization_format == SerializationFormat.TOML:
            import toml

            try:
                obj = toml.loads(s)

            except toml.TomlDecodeError as e:
                raise SerializationDecodeError(e)

        else:
            try:
                obj = json.loads(s)

            except JSONDecodeError as e:
                raise SerializationDecodeError(e)

        obj2tree_struct(self, obj, is_root_node=True)
        return

    def dump(self, fp, serialization_format=None):
        if isinstance(serialization_format, SerializationFormat):
            self._serialization_format = serialization_format

        s = self.dumps()

        fp.write(s)
        return

    def load(self, fp, serialization_format=None):
        if isinstance(serialization_format, SerializationFormat):
            self._serialization_format = serialization_format

        s = fp.read()

        self.loads(s)
        return
