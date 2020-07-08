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
from showops.utils import create_not_exists


def run_mysqldump(usr, pwd, host, port, backup_path, is_zip, db_name=None, table=None):
    """ 产生mysqldump命令，支持全库，单库，数据表备份语句
    """
    dump_cmd_temp = "mysqldump -u{usr} -p{pwd} -h{host} -P{port} {params} {source} > {target}"
    if db_name is None and table is None:
        # all databases backup
        source = ""
        target = os.path.join(backup_path, "all_databases.sql")
        default_params = "-A -B -F -R --master-data=2"
    elif table is not None:
        # tables backup
        source = "{} {}".format(db_name, table)
        target = os.path.join(backup_path, "table_{}.sql".format(table))
        default_params = ""
    elif db_name is not None:
        # one database backup
        source = "{}".format(db_name)
        target = os.path.join(backup_path, "db_{}.sql".format(db_name))
        default_params = "-B -F -R --master-data=2"

    if is_zip:
        source = "{}|gzip".format(source)
        target = "{}.gz".format(target)

    cmd = dump_cmd_temp.format(
        usr=usr, pwd=pwd, host=host, port=port, params=default_params, source=source, target=target
    )
    # os.system(cmd)
    print(cmd)


def backup(conf):
    # 定义备份文件夹生成规则 eg.'/backup/20170817_123205/database_name'
    today_path = os.path.join(conf["backup_path"], time.strftime("%Y%m%d_%H%M%S"))
    if not conf["source"]:
        # all databases backup if the DB_TARGET is empty
        backup_path = os.path.join(today_path, "all_databases")
        create_not_exists(backup_path)
        print("Starting backup of all databases")
        run_mysqldump(
            conf["usr"], conf["pwd"], conf["host"], conf["port"], backup_path, conf["is_zip"]
        )
        return

    for target in conf["source"]:
        db_name = target["db"]
        tables = target.get("tables", [])
        backup_path = os.path.join(today_path, db_name)
        create_not_exists(backup_path)
        if len(tables) > 0:
            for table in tables:
                print("Starting backup of table {}".format(table))
                run_mysqldump(
                    conf["usr"],
                    conf["pwd"],
                    conf["host"],
                    conf["port"],
                    backup_path,
                    conf["is_zip"],
                    db_name,
                    table,
                )
        else:
            print("Starting backup of database {}".format(db_name))
            run_mysqldump(
                conf["usr"],
                conf["pwd"],
                conf["host"],
                conf["port"],
                backup_path,
                conf["is_zip"],
                db_name,
            )
