================
TreeStructConfig
================

.. image:: https://img.shields.io/pypi/v/TreeStructConfig.svg
    :target: https://pypi.org/project/TreeStructConfig/
.. image:: https://img.shields.io/pypi/pyversions/TreeStructConfig.svg
    :target: https://pypi.org/project/TreeStructConfig/
.. image:: https://img.shields.io/pypi/dm/TreeStructConfig.svg
    :target: https://pypi.org/project/TreeStructConfig/


A Tree Struct Configuration module for python, support dump to/from JSON and TOML.


Install
=======

.. code-block:: console

    pip install -U TreeStructConfig


Usage
=====

Define class and create object

.. code-block:: python
    :number-lines:

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
      "version": "0.2.0",
      "Auth": {
        "username": "new_user"
      },
      "Wireless": {
        "AP": {
          "channel": 1,
          "enabled": true,
          "password": "new_password",
        }
      }
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
    :number-lines:

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

Demo source code: demo.py_

.. _demo.py: demo.py

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


Alternative
===========

* https://gitlab.com/alelec/structured_config
