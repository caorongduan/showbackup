#!/usr/bin/env python
# coding: UTF-8
# filename: utils.py

"""
utils.py
～～～～～

通用工具


:author: caorongduan@gmail.com
:copyright: 2017 caorongduan
:license: Apache2, see LICENSE for more details.
"""

import os
import json
import shutil
from datetime import datetime, timedelta


def create_not_exists(path):
    """ 创建目录 """
    if not os.path.exists(path):
        os.makedirs(path)


def delete_exists(path):
    """ 删除目录 """
    if os.path.isfile(path):
        os.remove(path)
    elif os.path.isdir(path):
        shutil.rmtree(path)


# with open("demo2.json", "w", encoding='utf-8') as f:
#     # json.dump(dict_var, f)  # 写为一行
#     json.dump(dict_var, f,indent=2,sort_keys=True, ensure_ascii=False)  # 写为多行


def read_from_json_file(path):
    """ 从json文件中读取，并转换为字典 """
    with open(path, encoding="utf-8") as json_file:
        obj = json.load(json_file)
        return obj


def delete_outdate_file(path, keep_days):
    """ 删除过期文件
        :param path 文件或目录路径，删除该目录下所有过期的文件，但保留本目录；如果为文件，直接删除文件
        :param keep_days 保留天数
    """
    if os.path.isfile(path):
        create_date = datetime.fromtimestamp(os.path.getctime(path))
        if is_outdate(create_date, keep_days):
            delete_exists(path)
    elif os.path.isdir(path):
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            create_date = datetime.fromtimestamp(os.path.getctime(file_path))
            if is_outdate(create_date, keep_days):
                delete_exists(file_path)


def is_outdate(create_date, keep_days):
    """ 判断是否过期
        :param create_date 创建日期
        :param keep_days 保留天数
        :returns True 过期， False未过期
    """
    if isinstance(create_date, datetime):
        outdate = create_date + timedelta(days=keep_days)
        return outdate < datetime.now()


def shell(cmd):
    """ 执行shell命令
        使用subprocess.Popen()替代陈旧的os.system() os.popen() etc.
    """
    import subprocess

    popen = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout = popen.stdout.readlines()
    stderr = popen.stderr.read()
    if isinstance(stderr, bytes):
        stderr = stderr.decode("utf-8")
    return stdout, stderr
