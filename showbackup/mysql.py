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
import schedule
from showbackup.utils import create_not_exists, delete_outdate_file, shell


class Mysql(object):
    def __init__(self, conf):
        self.conf = conf

    def check_conf(self, is_schedule=False):
        # 检查必填项
        required = ["usr", "pwd", "backup_path"]
        if is_schedule:
            required.append("every_day_at")
        if not all(k in self.conf and self.conf[k] for k in required):
            return False, "参数异常！请完成配置必填项：user, pwd, backup_path, every_day_at"

        # 设置默认值
        if not self.conf.get("host", ""):
            self.conf["host"] = "localhost"
        if not self.conf.get("port", 0):
            self.conf["port"] = 3306
        if not self.conf.get("keep_days", ""):
            self.conf["keep_days"] = "3"
        if not self.conf.get("source", []):
            self.conf["source"] = []
        if not self.conf.get("is_zip", True):
            self.conf["is_zip"] = True

        return True, ""

    def run_mysqldump(self, usr, pwd, host, port, backup_path, is_zip, db_name=None, table=None):
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
            usr=usr,
            pwd=pwd,
            host=host,
            port=port,
            params=default_params,
            source=source,
            target=target,
        )
        # print(cmd)
        shell(cmd)

    def backup(self):
        # 定义备份文件夹生成规则 eg.'/backup/20170817_123205/database_name'
        check_flag = self.check_conf()
        if not check_flag[0]:
            raise Exception(check_flag[1])
        today_path = os.path.join(self.conf["backup_path"], time.strftime("%Y%m%d_%H%M%S"))
        if not self.conf["source"]:
            # all databases backup if the DB_TARGET is empty
            backup_path = os.path.join(today_path, "all_databases")
            create_not_exists(backup_path)
            print("Starting backup of all databases")
            self.run_mysqldump(
                self.conf["usr"],
                self.conf["pwd"],
                self.conf["host"],
                self.conf["port"],
                backup_path,
                self.conf["is_zip"],
            )
            return

        for target in self.conf["source"]:
            db_name = target["db"]
            tables = target.get("tables", [])
            backup_path = os.path.join(today_path, db_name)
            create_not_exists(backup_path)
            if len(tables) > 0:
                for table in tables:
                    print("Starting backup of table {}".format(table))
                    self.run_mysqldump(
                        self.conf["usr"],
                        self.conf["pwd"],
                        self.conf["host"],
                        self.conf["port"],
                        backup_path,
                        self.conf["is_zip"],
                        db_name,
                        table,
                    )
            else:
                print("Starting backup of database {}".format(db_name))
                self.run_mysqldump(
                    self.conf["usr"],
                    self.conf["pwd"],
                    self.conf["host"],
                    self.conf["port"],
                    backup_path,
                    self.conf["is_zip"],
                    db_name,
                )

        # 删除过期文件
        keep_days = int(self.conf["keep_days"])
        if keep_days > 0:
            delete_outdate_file(self.conf["backup_path"], keep_days)

    def backup_schedule(self):
        check_flag = self.check_conf(is_schedule=True)
        if not check_flag[0]:
            raise Exception(check_flag[1])
        at_time = self.conf["every_day_at"]
        print("将于每天 {} 开始执行备份任务".format(at_time))
        schedule.every().day.at(at_time).do(self.backup)
        while True:
            schedule.run_pending()
            time.sleep(1)
