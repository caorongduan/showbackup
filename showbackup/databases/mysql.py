#!/user/bin/env python
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
import logging
import schedule
import configparser
from showbackup.utils import create_not_exists, delete_outdate_file, shell, the_moment_dirname
from showbackup.logger import get_logger
from showbackup.storages import Storage

logger = get_logger()


def parse_config(config_path):
    """ 根据配置文件路径，读取文件，获取mysql相关配置
        :returns dict
    """
    cf = configparser.ConfigParser()
    cf.read(config_path, encoding="utf-8")
    mysql_conf_list = cf.items("mysql")
    mysql_conf_dict = {item[0]: item[1] for item in mysql_conf_list}

    # 处理全局字段
    global_conf_list = cf.items("global")
    global_conf_dict = {item[0]: item[1] for item in global_conf_list}
    mysql_conf_dict["global"] = global_conf_dict

    # 处理source字段
    source = []
    source_lis = mysql_conf_dict["source"].split(",")
    for database in source_lis:
        if "*" in database:
            source = []
            break
        elif ":" in database:
            db_tables = database.split(":")
            source.append({"db": db_tables[0], "tables": db_tables[1:]})
        else:
            source.append({"db": database})
    mysql_conf_dict["source"] = source

    # 处理存储方式
    storage_conf_list = cf.items(mysql_conf_dict["storage"])
    storage_conf_dict = {item[0]: item[1] for item in storage_conf_list}
    mysql_conf_dict["storage"] = storage_conf_dict

    # 处理压缩
    mysql_conf_dict["is_zip"] = int(mysql_conf_dict["is_zip"])

    return mysql_conf_dict


class Mysql(object):
    def __init__(self, conf):
        self.conf = conf
        # 定义目标文件文件的列表，用于存储
        self.target_files = []

        # 此次备份以时间命名的文件夹名称
        self.moment_dir = the_moment_dirname()

        # 检测binlog是否开启
        try:
            self.is_binlog = self.is_supported_binlog()
        except Exception as e:
            logger.error("Error: {}".format(e), exc_info=True)
            exit()
        if not self.is_binlog:
            logger.warn("您尚未开启binlog，强烈建议您在生产环境中开启binlog...")

    def check_conf(self, is_schedule=False):
        # 检查必填项
        checked_params = []
        required = ["username", "password", "temp_path"]
        if is_schedule:
            required.append("every_day_at")

        # 检查参数，password允许为空
        for r in required:
            if r == "password":
                checked_params.append(r in self.conf)
            elif r == "temp_path":
                checked_params.append(r in self.conf["global"])
            else:
                checked_params.append(r in self.conf and self.conf[r])

        if not all(checked_params):
            return False, "参数异常！请完成配置必填项：username, password, backup_path, every_day_at"

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

    def is_supported_binlog(self):
        bin_log_cmd = """mysql -u{} -p{} -e 'show variables like "log_bin"'""".format(
            self.conf["username"], self.conf["password"]
        )
        result, error = shell(bin_log_cmd)
        if "Access denied" in error:
            raise Exception(
                "Access denied for user {}@{} 数据库账号密码有误，请重新设置".format(
                    self.conf["username"], self.conf["host"]
                )
            )
        for item in result:
            item_str = item.decode("utf-8").upper()
            if "LOG_BIN" in item_str and "ON" in item_str:
                return True
            elif "LOG_BIN" in item_str and "OFF" in item_str:
                return False
        return False

    def run_mysqldump(
        self, username, password, host, port, backup_path, is_zip, db_name=None, table=None
    ):
        """ 产生mysqldump命令，支持全库，单库，数据表备份语句
            备份库默认都加上 -R --triggers，避免生产环境备份，遗漏存储过程和触发器
        """
        default_params = "--master-data=2 --single-transaction" if self.is_binlog else ""
        dump_cmd_temp = (
            "mysqldump -u{username} -p{password} -h{host} -P{port} {params} {source} > {target}"
        )
        if db_name is None and table is None:
            # all databases backup
            source = ""
            target = os.path.join(backup_path, "all_databases.sql")
            default_params = "{} -A -B -R --triggers".format(default_params)
        elif table is not None:
            # tables backup
            source = "{} {}".format(db_name, table)
            target = os.path.join(backup_path, "table_{}.sql".format(table))
            default_params = ""
        elif db_name is not None:
            # one database backup
            source = "{}".format(db_name)
            target = os.path.join(backup_path, "db_{}.sql".format(db_name))
            default_params = "{} -B -R --triggers".format(default_params)

        if is_zip:
            source = "{}|gzip".format(source)
            target = "{}.gz".format(target)

        # 将临时目标文件存放至目标列表，用于存储
        self.target_files.append(target)

        cmd = dump_cmd_temp.format(
            username=username,
            password=password,
            host=host,
            port=port,
            params=default_params,
            source=source,
            target=target,
        )
        shell(cmd)

    def _backup_now(self):
        # 定义备份文件夹生成规则 eg.'/backup/20170817_123205/database_name'
        start_time = time.time()
        today_path = os.path.join(self.conf["global"]["temp_path"], self.moment_dir)

        if not self.conf["source"]:
            # all databases backup if the source is empty
            backup_path = os.path.join(today_path, "all_databases")
            create_not_exists(backup_path)
            logger.info("开始执行全库备份...")
            self.run_mysqldump(
                self.conf["username"],
                self.conf["password"],
                self.conf["host"],
                self.conf["port"],
                backup_path,
                self.conf["is_zip"],
            )
        else:
            for target in self.conf["source"]:
                db_name = target["db"]
                tables = target.get("tables", [])
                backup_path = os.path.join(today_path, db_name)
                create_not_exists(backup_path)
                if len(tables) > 0:
                    for table in tables:
                        logger.info("开始备份数据表：{}".format(table))
                        self.run_mysqldump(
                            self.conf["username"],
                            self.conf["password"],
                            self.conf["host"],
                            self.conf["port"],
                            backup_path,
                            self.conf["is_zip"],
                            db_name,
                            table,
                        )
                else:
                    logger.info("开始备份数据库：{}".format(db_name))
                    self.run_mysqldump(
                        self.conf["username"],
                        self.conf["password"],
                        self.conf["host"],
                        self.conf["port"],
                        backup_path,
                        self.conf["is_zip"],
                        db_name,
                    )

        # 处理存储逻辑
        self._do_storage()

        logger.info("所有任务均已完成，总耗时{:.2f}秒".format(time.time() - start_time))
        return

    def _backup_schedule(self):
        at_time = self.conf["every_day_at"]
        logger.info("将于每天 {} 开始执行备份任务".format(at_time))
        schedule.every().day.at(at_time).do(self._backup_now)
        while True:
            schedule.run_pending()
            time.sleep(1)

    def backup(self, is_schedule=False):
        # 先做参数检查
        check_flag = self.check_conf(is_schedule)
        if not check_flag[0]:
            logger.error(check_flag[1])
            exit()
        if is_schedule:
            self._backup_schedule()
        else:
            self._backup_now()

    def _do_storage(self):
        """ 调用存储，处理存储工作
        """
        ext = self.conf["storage"]["type"]
        kwargs = self.conf["storage"]
        kwargs["root"] = self.conf["global"]["temp_path"]
        kwargs["data_dir"] = self.moment_dir
        s = Storage.create(ext, kwargs)
        s.storage()
