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

from showops.mysql import backup
from showops.utils import read_from_json_file


if __name__ == "__main__":
    config_path = "./conf.json"
    conf_dict = read_from_json_file(config_path)
    mysql_conf = conf_dict.get("mysql", {})

    backup(mysql_conf)
