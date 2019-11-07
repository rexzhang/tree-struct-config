#!/usr/bin/env python
# coding=utf-8


from tree_struct_config import (
    IntLeaf,
    StringLeaf,
    BooleanLeaf,
    ListLeaf,

    BranchNode,

    RootNode,
    SerializationFormat,
    SerializationDecodeError,
)


class Config(RootNode):
    version = StringLeaf('0.1.0')

    class Auth(BranchNode):
        username = StringLeaf('rex')
        password = StringLeaf('password')

    class Wireless(BranchNode):
        class AP(BranchNode):
            enabled = BooleanLeaf(True)
            channel = IntLeaf(1)
            password = StringLeaf('password')
            mac_acl_list = ListLeaf([
                '00:00:00:00:00:00',
            ])

    class NotExistBranch(BranchNode):
        pass

    not_exist_leaf = StringLeaf()


class AdvancedConfig(Config):
    """override dump/load function"""
    _filename = None

    def dump(self, fp=None, serialization_format=None):
        with open(self._filename, 'w') as fp:
            super().dump(fp, serialization_format)

        return

    def load(self, fp=None, serialization_format=None):
        with open(self._filename) as fp:
            try:
                super().load(fp, serialization_format)

            except SerializationDecodeError:
                pass


# basic usage
config = Config()

data = '''
{
  "Auth": {
    "password": "xxxxxxxx",
    "username": "admin"
  },
  "Wireless": {
    "AP": {
      "channel": 1,
      "enabled": true,
      "hw_mode": "n",
      "interface": "uap0",
      "password": "xxxxxxxx",
      "ssid": "PiRouter"
    },
    "Client": {
      "enabled": false,
      "password": "xxxxxxxx",
      "ssid": "ssid"
    }
  }
}

'''

print('----------')
print(config.Wireless.AP.password)
config.Wireless.AP.password = 'new_password'
print(config.Wireless.AP.password)

# dumps/loads/dump/load as python.json module
print('----------')
print(config.dumps())

print('----------')
config.loads(data)
print(config.Wireless.AP.password)

with open('demo.json', 'w') as f:
    config.dump(f)

with open('demo.json') as f:
    config.load(f)

# override dump/load func
advanced_config = AdvancedConfig()
advanced_config._filename = 'demo.toml'
advanced_config.dump(serialization_format=SerializationFormat.TOML)
advanced_config.load(serialization_format=SerializationFormat.TOML)
