#!/usr/bin/env python
# coding=utf-8


import json
from enum import Enum

ROOT_NODE_FUNC_NAME_SET = {'dump', 'dumps', 'load', 'loads'}


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
    default = None
    value = None

    def __init__(self, default=None):
        if default is None:
            self.value = self.default

        else:
            self.value = default

    def __get__(self, instance, owner):
        # print('<<< get', instance, owner)
        return self.value

    def __set__(self, instance, value):
        print('>>> set', instance, value)
        self.value = 'value'

    # def __delete__(self, instance):
    #     print('!!! delete')
    #
    # def __setattr__(self, key, value):
    #     print('>>>', key, value)
    #     super().__setattr__(key, value)


class IntLeaf(LeafNode):
    default = 0


class StringLeaf(LeafNode):
    default = ''


class BooleanLeaf(LeafNode):
    default = False


class BranchNode(NodeBase, metaclass=BranchNodeMetaClass):
    _node_type = NodeType.BRANCH


def _obj2data(cls, is_root_node=False):
    data = {}

    for child_node_name in dir(cls):
        if child_node_name[0] == '_':
            continue

        if is_root_node and child_node_name in ROOT_NODE_FUNC_NAME_SET:
            continue

        child_node = getattr(cls, child_node_name)

        if type(child_node) == type(BranchNode):
            # NodeType.BRANCH
            data[child_node_name] = _obj2data(child_node)

        # elif type(child_node) == type(RootNode):
        #     # NodeType.ROOT
        #     # raise('!!!!')
        #     print('!!!!!!')
        #     continue

        else:
            # NodeType.LEAF
            data[child_node_name] = child_node

    return data


def _data2obj(cls, data, is_root_node=False):
    for child_node_name in dir(cls):
        if child_node_name[0] == '_':
            continue

        if is_root_node and child_node_name in ROOT_NODE_FUNC_NAME_SET:
            continue

        child_node = getattr(cls, child_node_name)

        if type(child_node) == type(BranchNode):
            # NodeType.BRANCH
            _data2obj(child_node, data[child_node_name])

        else:
            # NodeType.LEAF
            if child_node_name not in data:
                continue

            setattr(cls, child_node_name, data[child_node_name])

    return


class RootNode(NodeBase, metaclass=RootNodeMetaClass):
    _node_type = NodeType.ROOT

    def dumps(self):
        data = _obj2data(self, is_root_node=True)

        return json.dumps(data, indent=2)

    def dump(self, fp):
        data = _obj2data(self, is_root_node=True)

        return json.dump(obj=data, fp=fp, indent=2)

    def loads(self, s):
        data = json.loads(s)

        _data2obj(self, data, is_root_node=True)
        return

    def load(self, fp, s):
        data = json.load(fp=fp, s=s)

        _data2obj(self, data, is_root_node=True)
        return
