#!/usr/bin/env python
# coding: UTF-8
# filename: file.py

"""
Mysql数据备份脚本

Author: caorongduan@gmail.com
Copyright: 2017 caorongduan
License: Apache2, see LICENSE for more details.
Version: 1.0
"""

import json
from showops.mysql import backup


if __name__ == "__main__":
    mysql_conf = None
    with open("./conf.json", "r") as conf_json:
        conf_dict = json.loads(conf_json.read())
        mysql_conf = conf_dict["mysql"]

    backup(mysql_conf)
