#!/usr/bin/env python
# coding=utf-8


from tree_view_config import (
    IntLeaf,
    StringLeaf,
    BooleanLeaf,

    BranchNode,
    RootNode,
)


class Config(RootNode):
    info = StringLeaf('some info')

    class Auth(BranchNode):
        username = StringLeaf('admin')
        password = StringLeaf('password')

    class Wireless(BranchNode):
        class AP(BranchNode):
            enabled = BooleanLeaf(True)

            interface = StringLeaf('uap0')  # DON'T CHANGE IT
            ssid = StringLeaf('PiRouter')
            password = StringLeaf('password')
            hw_mode = StringLeaf('n')
            channel = IntLeaf(1)


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

print(config.info)
print(config.Wireless.AP.password)
config.Wireless.AP.password = 'new_password'
print(config.dumps())

config.loads(data)
print(config.Wireless.AP.password)

with open('demo.json', 'w') as f:
    config.dump(f)
