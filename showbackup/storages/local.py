#!/usr/bin/env python
# coding: UTF-8
# filename: local.py

"""
local.py

:author: caorongduan@gmail.com
:copyright: 2017 caorongduan
:license: Apache2, see LICENSE for more details.
"""

import os
import shutil
from showbackup.logger import get_logger
from showbackup.utils import shell, create_not_exists, delete_exists, delete_outdate_file

logger = get_logger()


class Local(object):
    def __init__(self, kwargs):
        """ 参数合法性检查并进行属性赋值
        """
        # allowed 参数说明
        # type: 小写类名
        # path: 目标存储目录
        # keep: 历史备份文件保留天数
        # root: 源数据的所在目录
        # data_dir: 数据源目录（根目录下的数据目录）
        allowed = ("type", "path", "keep", "root", "data_dir")
        for kwarg in kwargs:
            assert kwarg in allowed, "Invalid keyword argument: {}".format(kwarg)
        self.__dict__.update(kwargs)

    def storage(self):
        source = os.path.join(self.root, self.data_dir)
        shutil.move(source, self.path)
        self._clear()
        logger.info("{}存储完成，目标路径:{}".format(self.type, self.path))

    def _clear(self):
        # 删除过期文件
        keep_days = int(self.keep)
        if keep_days > 0:
            logger.info("正在检查过期备份文件...")
            delete_outdate_file(self.path, keep_days)
            return
        logger.info("无需处理过期备份文件...")
        return
