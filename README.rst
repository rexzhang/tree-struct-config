==============
TreeViewConfig
==============

.. image:: https://img.shields.io/pypi/v/TreeViewConfig.svg
    :target: https://pypi.org/project/TreeViewConfig/
.. image:: https://img.shields.io/pypi/pyversions/TreeViewConfig.svg
    :target: https://pypi.org/project/TreeViewConfig/
.. image:: https://img.shields.io/pypi/dm/TreeViewConfig.svg
    :target: https://pypi.org/project/TreeViewConfig/


A configuration module for python, support dump from/to JSON.


Install
=======

.. code-block:: console

    pip install TreeViewConfig


Usage
=====

.. code-block:: python

    from tree_view_config import RootNode, BranchNode, StringLeaf, IntLeaf, BooleanLeaf


    class Config(RootNode):
        username = StringLeaf('admin')
        password = StringLeaf('password')

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

            class Client(BranchNode):
                enabled = BooleanLeaf(False)

                ssid = StringLeaf('ssid')
                password = StringLeaf('password')


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

    config = Config()
    print(config.dumps())

    print('--------')
    config.loads(data)
    print(config.Wireless.AP.password)


.. code-block:: bash

    {
      "Auth": {
        "password": "password",
        "username": "admin"
      },
      "Wireless": {
        "AP": {
          "channel": 1,
          "enabled": true,
          "hw_mode": "n",
          "interface": "uap0",
          "password": "password",
          "ssid": "PiRouter"
        },
        "Client": {
          "enabled": false,
          "password": "password",
          "ssid": "ssid"
        }
      },
      "password": "password",
      "username": "admin"
    }
    --------
    xxxxxxxx


Alternative
===========

* https://gitlab.com/alelec/structured_config
