#!/usr/bin/env python
# coding=utf-8


from tree_struct_config import (
    IntLeaf,
    StringLeaf,
    BooleanLeaf,

    BranchNode,
    RootNode,

    ConfigDecodeError,
)


class Config(RootNode):
    version = StringLeaf('0.1.0')

    class Auth(BranchNode):
        username = StringLeaf('admin')
        password = StringLeaf('password')

    class Wireless(BranchNode):
        class AP(BranchNode):
            enabled = BooleanLeaf(True)
            channel = IntLeaf(1)
            password = StringLeaf('password')


class AdvancedConfig(Config):
    """override dump/load function"""
    _filename = None

    def dump(self, fp=None):
        with open(self._filename, 'w') as fp:
            super().dump(fp)

        return

    def load(self, fp=None):
        with open(self._filename) as fp:
            try:
                super().load(fp)

            except ConfigDecodeError:
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
advanced_config._filename = 'demo.json'
advanced_config.dump()
advanced_config.load()
