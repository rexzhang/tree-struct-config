#!/usr/bin/env bash

pip install -U wheel pip twine


rm -rf build dist
python setup.py sdist bdist_wheel
