#!/usr/bin/env python
# coding: UTF-8
# filename: scp.py

"""
scp.py

:author: caorongduan@gmail.com
:copyright: 2017 caorongduan
:license: Apache2, see LICENSE for more details.
"""


class Scp(object):
    def __init__(self, conf):
        self.conf = conf

    def storage(self):
        print("i am scp")
        print(self.conf)
