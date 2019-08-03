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

Source code: demo.py_

.. _demo.py: blob/master/demo.py

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
