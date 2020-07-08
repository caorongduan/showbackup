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
import json
import shutil


def create_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


def delete_exists(path):
    if os.path.isfile(path):
        os.remove(path)
    elif os.path.isdir(path):
        shutil.rmtree(path)


def read_from_json_file(path=None):
    if path is None:
        return {}
    with open(path, "r") as json_file:
        obj = json.loads(json_file.read())
        return obj
