from typing import List

import pytest

from tree_struct_config.core2 import Root, Branch

t_str_alpha = 'alpha'
t_str_beta = 'beta'
t_str_gamma = 'gamma'
t_bool_true = True
t_int_1 = 1
t_list_str = [
    '00:00:00:00:00:00',
    '11:11:11:11:11:11',
]
t_list_list_str = [
    ['00:00:00:00:00:00', 'a'],
    ['11:11:11:11:11:11', 'b'],
]


class ConfigA(Root):
    str_item: str = t_str_alpha

    class Sub1(Branch):
        str_item: str = t_str_beta

    class Sub2(Branch):
        class Sub2Sub1(Branch):
            str_item: str = t_str_gamma
            bool_item: bool = t_bool_true
            int_item: int = t_int_1
            list_item: List[str] = t_list_str

    class NotExistBranch:
        pass

    not_exist_item: str


@pytest.fixture
def config_a():
    config = ConfigA()
    config.str_item = t_str_alpha
    config.Sub1.str_item = t_str_beta
    config.Sub2.Sub2Sub1.str_item = t_str_gamma
    return config


def test_str(config_a):
    new_str = 'new_str'

    assert type(config_a.str_item) == str
    assert config_a.str_item == t_str_alpha

    config_a.str_item = new_str
    assert config_a.str_item == new_str

    temp = config_a.str_item
    assert temp == new_str

    # sub
    assert type(config_a.Sub1.str_item) == str
    assert config_a.Sub1.str_item == t_str_beta

    config_a.Sub1.str_item = new_str
    assert config_a.Sub1.str_item == new_str

    temp = config_a.Sub1.str_item
    assert temp == new_str

    # sub-sub
    assert type(config_a.Sub2.Sub2Sub1.str_item) == str
    assert config_a.Sub2.Sub2Sub1.str_item == t_str_gamma

    config_a.Sub2.Sub2Sub1.str_item = new_str
    assert config_a.Sub2.Sub2Sub1.str_item == new_str

    temp = config_a.Sub2.Sub2Sub1.str_item
    assert temp == new_str


def test_dumps_json(config_a):
    dump_str = config_a.dumps()
    # print(dump_str)
    assert dump_str == """{
  "NotExistBranch": null,
  "Sub1": {
    "str_item": "beta"
  },
  "Sub2": {
    "Sub2Sub1": {
      "bool_item": true,
      "int_item": 1,
      "list_item": [
        "00:00:00:00:00:00",
        "11:11:11:11:11:11"
      ],
      "str_item": "gamma"
    }
  },
  "str_item": "alpha"
}"""

    config_a.str_item = 'new_value'
    config_a.Sub2.Sub2Sub1.str_item = 'new_value2'
    dump_str = config_a.dumps()
    # print(dump_str)
    assert dump_str == """{
  "NotExistBranch": null,
  "Sub1": {
    "str_item": "beta"
  },
  "Sub2": {
    "Sub2Sub1": {
      "bool_item": true,
      "int_item": 1,
      "list_item": [
        "00:00:00:00:00:00",
        "11:11:11:11:11:11"
      ],
      "str_item": "new_value2"
    }
  },
  "str_item": "new_value"
}"""


def test_loads(config_a):
    dump_str = """{
  "NotExistBranch": null,
  "Sub1": {
    "str_item": "beta"
  },
  "Sub2": {
    "Sub2Sub1": {
      "bool_item": true,
      "int_item": 1,
      "list_item": [
        "00:00:00:00:00:00",
        "11:11:11:11:11:11"
      ],
      "str_item": "new_value2"
    }
  },
  "str_item": "new_value"
}"""
    assert config_a.str_item == t_str_alpha
    assert config_a.Sub2.Sub2Sub1.str_item == t_str_gamma
    config_a.loads(dump_str)
    assert config_a.str_item == 'new_value'
    assert config_a.Sub2.Sub2Sub1.str_item == 'new_value2'
