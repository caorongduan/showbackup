#!/usr/bin/env python
# coding: UTF-8
# filename: utils.py

"""
utils.py
～～～～～

通用工具


:author: caorongduan@gmail.com
:copyright: 2017 caorongduan
:license: Apache2, see LICENSE for more details.
"""

import os


def create_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
