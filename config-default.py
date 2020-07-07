#!/usr/bin/env python
# coding: UTF-8
# filename: config.py

""" 定义一些配置
:author: caorongduan@gmail.com
:copyright: 2017 caorongduan
:license: Apache2, see LICENSE for more details.
"""


class MysqlConfig:
    """ Mysql配置文件参数说明

        source
            - 为空字典，则表示备份所有数据库
            - 里面的item如果仅指定了db，没有指定tables，或者tables为空列表，则表示备份单数据库
            - 里面的item如果指定了db，也指定了tables，则表示仅备份该数据库的指定表
        backup_path:
            - 备份文件的路径
        is_gzip
            - True为压缩，输出*.sql.gz，False为输出sql文件
    """

    host = "localhost"
    port = "3306"
    user = "root"
    password = ""
    source = {
        {"db": "test01", tables: ["table01", "table02"]},
        {"db": "test02", tables: []},
        {"db": "test03"},
    }
    backup_path = "./"
    is_gzip = True
