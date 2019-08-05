================
TreeStructConfig
================

.. image:: https://img.shields.io/pypi/v/TreeStructConfig.svg
    :target: https://pypi.org/project/TreeStructConfig/
.. image:: https://img.shields.io/pypi/pyversions/TreeStructConfig.svg
    :target: https://pypi.org/project/TreeStructConfig/
.. image:: https://img.shields.io/pypi/dm/TreeStructConfig.svg
    :target: https://pypi.org/project/TreeStructConfig/


A Tree Struct Configuration module for python, support dump to/from JSON/TOML(todo).


Install
=======

.. code-block:: console

    pip install TreeStructConfig


Usage
=====

Create object
-------------

.. code-block:: python
    :number-lines:

    class Config(RootNode):
        version = StringLeaf('0.1.0')

        class Auth(BranchNode):
            username = StringLeaf('admin')

        class Wireless(BranchNode):
            class AP(BranchNode):
                enabled = BooleanLeaf(True)
                channel = IntLeaf(1)
                password = StringLeaf('password')

    config = Config()

Access config value
-------------------

.. code-block:: python
    :number-lines:

    username = config.Auth.username

Update config value
-------------------

.. code-block:: python
    :number-lines:

    config.Auth.username = 'rex'
    config.Wireless.AP.password = 'new_password'


Dump config to JSON
-------------------

code

.. code-block:: python
    :number-lines:

    print(config.dumps())

output

.. code-block:: console

    {
      "version": "0.1.0",
      "Auth": {
        "username": "rex"
      },
      "Wireless": {
        "AP": {
          "channel": 1,
          "enabled": true,
          "password": "new_password",
        }
      }
    }


Load config from JSON
---------------------

code

.. code-block:: python
    :number-lines:

    json_str = """
    {
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
    """
    config.loads(json_str)
    print(config.Auth.username")

output

.. code-block:: console

    new_user


Demo
====

Source code: demo.py_

.. _demo.py: demo.py

.. include:: demo.py
    :code: python
    :number-lines:

Output

.. code-block:: console

    ----------
    password
    new_password
    ----------
    {
      "Auth": {
        "password": "password",
        "username": "admin"
      },
      "Wireless": {
        "AP": {
          "channel": 1,
          "enabled": true,
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
