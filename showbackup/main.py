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
import logging
from showbackup.databases.mysql import Mysql
from showbackup.utils import read_from_json_file
from showbackup.logger import get_logger
from showbackup import __version__

CONFIG_FILENAME = "conf.json"

logger = get_logger()


def get_root_path():
    # 获取项目根路径
    path = os.path.abspath(os.path.dirname(__file__))
    return path


def config_exsits():
    # 检查配置文件是否存在
    config_path = os.path.join(get_root_path(), CONFIG_FILENAME)
    return os.path.exists(config_path)


def edit_config(tips):
    config_cmd = "vi {}".format(os.path.join(get_root_path(), CONFIG_FILENAME))
    click.echo(click.style("{}\n{}\n".format(tips, config_cmd), fg="yellow"))


def get_version():
    full_version = "showbackup (version {})".format(__version__)
    return full_version


@click.group(invoke_without_command=True)
@click.option("--config", is_flag=True, default=False, help="编辑showbackup配置文件")
@click.option("--version", "-v", is_flag=True, default=False, help="显示版本信息")
def cli(config, version):
    """ showbackup: 一个短小精干的mysql数据库备份工具 """
    if config:
        # 编辑配置文件
        edit_config("请通过编辑showbackup配置文件来完成配置")
        return
    if version:
        # 显示版本信息
        click.echo(get_version())
        return


@cli.command()
@click.option("--schedule", "-s", is_flag=True, default=False, help="启用定时执行备份任务")
def mysql(schedule):
    """ 使用mysql子命令来对mysql进行数据备份"""
    if not config_exsits():
        edit_config("没有找到showbackup默认配置文件，请先创建并编辑")
        return
    config_full_path = os.path.join(get_root_path(), CONFIG_FILENAME)
    conf_dict = read_from_json_file(config_full_path)
    mysql_conf = conf_dict.get("mysql", {})
    if not mysql_conf:
        edit_config("没有找到mysql备份相关的配置项，请编辑配置文件")
        return
    mysql = Mysql(mysql_conf)
    if not schedule:
        tips = "为了保证数据的一致性，showbackup可能会进行锁表操作，一旦锁表将会影响数据库的写入，确定继续吗？"
        if click.confirm(tips):
            mysql.backup(schedule)
    else:
        mysql.backup(schedule)


if __name__ == "__main__":
    cli()
