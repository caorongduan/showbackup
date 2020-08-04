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
import shutil
import logging
from showbackup.databases.mysql import Mysql, parse_config
from showbackup.utils import read_from_json_file, shell
from showbackup.logger import get_logger
from showbackup import __version__

CONFIG_FILENAME = "/etc/showbackup.conf"

logger = get_logger()


def get_root_path():
    # 获取项目根路径
    path = os.path.abspath(os.path.dirname(__file__))
    return path


def config_exsits():
    # 检查配置文件是否存在
    config_path = os.path.join(get_root_path(), CONFIG_FILENAME)
    return os.path.exists(config_path)


def init_config():
    path = shutil.copy("./default.conf", CONFIG_FILENAME)
    if path == CONFIG_FILENAME:
        click.echo("初始化配置文件成功...\n修改配置文件运行： sudo vi {}".format(CONFIG_FILENAME))


def edit_config(tips):
    if not config_exsits():
        click.echo(
            click.style("{}不存在，请运行 showbackup --init 自动创建".format(CONFIG_FILENAME), fg="yellow")
        )
        return
    config_cmd = "sudo vi {}".format(CONFIG_FILENAME)
    click.echo(click.style("{}\n{}\n".format(tips, config_cmd), fg="yellow"))


def get_version():
    full_version = "showbackup (version {})".format(__version__)
    return full_version


@click.group(invoke_without_command=True)
@click.option("--init", is_flag=True, default=False, help="初始化showbackup配置文件")
@click.option("--config", is_flag=True, default=False, help="编辑showbackup配置文件")
@click.option("--version", "-v", is_flag=True, default=False, help="显示版本信息")
def cli(init, config, version):
    """ showbackup: 一个短小精干的mysql数据库备份工具 """
    if init:
        # 初始化配置文件
        tips = "初始化配置文件，将会覆盖已存在的配置文件，确认要继续吗？"
        if click.confirm(tips):
            init_config()
        return
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
        edit_config("没有找到showbackup默认配置文件，请运行 sudo showbackup --init 创建并编辑")
        return
    mysql_conf = parse_config(CONFIG_FILENAME)
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
    # from showbackup.databases.mysql import parse_config
    # from showbackup.storages import Storage
    #
    # temp = parse_config("./default.conf")
    # storage_conf = temp["storage"]
    # print(storage_conf)
    # s = Storage.create(storage_conf["type"], storage_conf)
    # s.storage()
