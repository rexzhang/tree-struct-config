================
TreeStructConfig
================

.. image:: https://img.shields.io/pypi/v/TreeStructConfig.svg
    :target: https://pypi.org/project/TreeStructConfig/
.. image:: https://img.shields.io/pypi/pyversions/TreeStructConfig.svg
    :target: https://pypi.org/project/TreeStructConfig/
.. image:: https://img.shields.io/pypi/dm/TreeStructConfig.svg
    :target: https://pypi.org/project/TreeStructConfig/


A Tree Struct Configuration module for python, support serialization to/from JSON and TOML.


Install
=======

Serialization with JSON

.. code-block:: console

    pip install -U TreeStructConfig

Serialization with TOML

.. code-block:: console

    pip install -U TreeStructConfig[toml]


Usage
=====

Define class and create object

.. code-block:: python

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


    config = Config()


Access config value

    >>> config.Auth.username
    rex
    >>> username = config.Auth.username
    >>> username
    rex


Update config value

    >>> config.Auth.username = 'new_user'
    >>> config.Auth.username
    new_user
    >>> config.Wireless.AP.password = 'new_password'
    >>> config.Wireless.AP.password
    new_password


Dump config to JSON string

    >>> config.dumps()
    {
      "Auth": {
        "password": "password",
        "username": "rex"
      },
      "Wireless": {
        "AP": {
          "channel": 1,
          "enabled": true,
          "mac_acl_list": [
            "00:00:00:00:00:00"
          ],
          "password": "new_password"
        }
      },
      "version": "0.1.0"
    }


Load config from JSON string

    >>> json_str = """
    ...     {
    ...       "Auth": {
    ...         "username": "new_user"
    ...       },
    ...       "Wireless": {
    ...         "AP": {
    ...           "channel": 1,
    ...           "enabled": true,
    ...           "password": "new_password",
    ...         }
    ...       }
    ...     }
    ... """
    ...
    >>> config.Auth.username
    rex
    >>> config.loads(json_str)
    >>> config.Auth.username
    new_user


Dump config to JSON file

    >>> with open('config.json', 'w') as f:
    ...     config.dump(f)


Load config from JSON file

    >>> with open('config.json') as f:
    ...     config.load(f)


Dump to TOML and load from TOML string and file

    >>> config.dumps(serialization_format=SerializationFormat.TOML)
    >>> config.loads(s, serialization_format=SerializationFormat.TOML)

    >>> with open('config.toml', 'w') as f:
    ...     config.dump(f, serialization_format=SerializationFormat.TOML)
    >>> with open('config.toml') as f:
    ...     config.load(f, serialization_format=SerializationFormat.TOML)

config.toml

.. code-block:: text

    version = "0.1.0"

    [Auth]
    password = "password"
    username = "rex"

    [Wireless.AP]
    channel = 1
    enabled = true
    mac_acl_list = [ "00:00:00:00:00:00",]
    password = "password"


Override ``dump()`` and ``load()`` function

.. code-block:: python

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


    advanced_config = AdvancedConfig()
    advanced_config._filename = 'config.json'
    advanced_config.dump()
    advanced_config.load()


Demo
====

Demo source code: https://github.com/rexzhang/tree-struct-config/blob/master/demo.py

Output

.. code-block:: console

    ----------
    password
    new_password
    ----------
    {
      "Auth": {
        "password": "password",
        "username": "rex"
      },
      "Wireless": {
        "AP": {
          "channel": 1,
          "enabled": true,
          "mac_acl_list": [
            "00:00:00:00:00:00"
          ],
          "password": "new_password"
        }
      },
      "version": "0.1.0"
    }
    ----------
    xxxxxxxx


Changelog
=========

0.2.3
-----
* Add new implement, depend typing hint(draft)

0.2.2
-----
* Fix not exist branch crash

0.2.1
-----
* Fix bug

0.2.0
-----
* Support TOML format file

0.1.0
-----
* First release

Alternative
===========

* https://gitlab.com/alelec/structured_config
