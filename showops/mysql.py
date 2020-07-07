#!/usr/bin/env python
# coding: UTF-8
# filename: mysql.py

"""
mysql.py
～～～～～

mysql相关功能

:author: caorongduan@gmail.com
:copyright: 2017 caorongduan
:license: Apache2, see LICENSE for more details.
"""

import os
import time
from config import MysqlConfig
from showops.utils import create_not_exists


def make_dump_cmd(path, db_name=None, table=None):
    """ 产生mysqldump命令，支持全库，单库，数据表备份语句
    """
    dump_cmd_temp = (
        "mysqldump -u{username} -p{password} {params} {source} > {target}"
    )
    if db_name is None and table is None:
        # all databases backup
        source = ""
        target = os.path.join(path, "all_databases.sql")
        default_params = "-A -B -F -R --master-data=2"
    elif table is not None:
        # tables backup
        source = "{} {}".format(db_name, table)
        target = os.path.join(path, "table_{}.sql".format(table))
        default_params = ""
    elif db_name is not None:
        # one database backup
        source = "{}".format(db_name)
        target = os.path.join(path, "db_{}.sql".format(db_name))
        default_params = "-B -F -R --master-data=2"

    if MysqlConfig.is_gzip:
        source = "{}|gzip".format(source)
        target = "{}.gz".format(target)

    cmd = dump_cmd_temp.format(
        username=MysqlConfig.user,
        password=MysqlConfig.password,
        params=default_params,
        source=source,
        target=target,
    )
    return cmd


def backup():
    # 定义备份文件夹生成规则 eg.'/backup/20170817_123205/database_name'
    today_path = os.path.join(
        MysqlConfig.backup_path, time.strftime("%Y%m%d_%H%M%S")
    )
    if not MysqlConfig.source:
        # all databases backup if the DB_TARGET is empty
        path = os.path.join(today_path, "all_databases")
        create_not_exists(path)
        cmd = make_dump_cmd(path)
        print("Starting backup of all databases")
        return os.system(cmd)

    for target in MysqlConfig.source:
        db_name = target["db"]
        tables = target.get("tables", [])
        path = os.path.join(today_path, db_name)
        create_not_exists(path)
        if len(tables) > 0:
            for table in tables:
                cmd = make_dump_cmd(path, db_name, table)
                print("Starting backup of table {}".format(table))
                os.system(cmd)
        else:
            cmd = make_dump_cmd(path, db_name)
            print("Starting backup of database {}".format(db_name))
            os.system(cmd)
