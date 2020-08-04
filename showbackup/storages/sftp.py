#!/usr/bin/env python
# coding: UTF-8
# filename: sftp.py

"""
sftp.py

:author: caorongduan@gmail.com
:copyright: 2017 caorongduan
:license: Apache2, see LICENSE for more details.
"""


class Sftp(object):
    def __init__(self, conf):
        self.conf = conf

    def storage(self):
        print("i am sftp")
        print(self.conf)
