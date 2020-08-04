#!/usr/bin/env python
# coding: UTF-8
# filename: __init__.py

"""
__init__.py
～～～～～

:author: caorongduan@gmail.com
:copyright: 2017 caorongduan
:license: Apache2, see LICENSE for more details.
"""

import importlib


class Storage(object):
    @staticmethod
    def create(storage, kwargs):
        """ A factory method for create an object of storages

            :author caorongduan@gmail.com
            :returns an storage object
        """
        exc_list = ["local", "ftp", "sftp", "scp"]
        if storage not in exc_list:
            raise Exception("unsuported storage type")

        # module = importlib.import_module("." + storage.lower(), "storages")
        module = importlib.import_module("showbackup.storages." + storage.lower())
        return getattr(module, storage.capitalize())(kwargs)
