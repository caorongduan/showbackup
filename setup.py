#!/usr/bin/env python
# coding: UTF-8
# filename: setup.py

"""
setup.py
～～～～～

:author: caorongduan@gmail.com
:copyright: 2017 caorongduan
:license: Apache2, see LICENSE for more details.
"""

from setuptools import setup

setup(
    name="showbackup",
    version="0.1.0",
    py_modules=["app"],
    install_requires=["Click", "schedule"],
    entry_points="""
        [console_scripts]
        showbackup=app:cli
    """,
)
