#!/usr/bin/env python
# coding: UTF-8
# filename: ftp.py

"""
ftp.py
～～～～～

:author: caorongduan@gmail.com
:copyright: 2017 caorongduan
:license: Apache2, see LICENSE for more details.
"""


class Ftp(object):
    def __init__(self, kwargs):
        """ 参数合法性检查并进行属性赋值
        """
        allowed = ("type", "path", "username", "password", "host", "port", "keep")
        for kwarg in kwargs:
            assert kwarg in allowed, "Invalid keyword argument: {}".format(kwarg)
        self.__dict__.update(kwargs)

    def storage(self):
        print(self.type)
        print(self.path)
        print(self.username)
        print(self.password)
        print(self.host)
        print(self.port)
        print(self.keep)
