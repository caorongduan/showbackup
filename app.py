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

import os
import click
from showbackup.mysql import Mysql
from showbackup.utils import read_from_json_file

config_filename = "example.conf.json"


def get_root_path():
    # 获取项目根路径
    path = os.path.abspath(os.path.dirname(__file__))
    return path


def config_exsits():
    # 检查配置文件是否存在
    config_path = os.path.join(get_root_path(), config_filename)
    return os.path.exists(config_path)


def edit_config(tips):
    config_cmd = "vi {}".format(os.path.join(get_root_path(), config_filename))
    click.echo("{}\n{}\n".format(tips, config_cmd))


@click.group()
def cli():
    pass


@cli.command()
@click.option("--config", is_flag=True, default=False, help="编辑showbackup配置文件")
@click.option("--schedule", "-s", is_flag=True, default=False, help="启用定时执行备份任务")
def mysql(config, schedule):
    """ showbackup 支持全库，指定库，指定表，定时快速备份。"""
    if config:
        # 编辑配置文件
        edit_config("请编辑showbackup配置文件")
        return
    if not config_exsits():
        edit_config("没有找到showbackup默认配置文件，请先创建并编辑")
        return
    conf_dict = read_from_json_file(config_filename)
    mysql_conf = conf_dict.get("mysql", {})
    if not mysql_conf:
        edit_config("没有找到mysql备份相关的配置项，请编辑配置文件")
        return
    mysql = Mysql(mysql_conf)
    if schedule:
        mysql.backup_schedule()
    else:
        mysql.backup()


if __name__ == "__main__":
    cli()
