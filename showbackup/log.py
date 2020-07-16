#!/usr/bin/env python
# coding: UTF-8
# filename: log.py

"""
log.py
～～～～～

处理统一日志

Usage:
    >>> from showbackup.log import get_logger
    >>> logger = get_logger()
    >>> logger.info('helloworld')

:author: caorongduan@gmail.com
:copyright: 2017 caorongduan
:license: Apache2, see LICENSE for more details.
"""

import os
import logging
import logging.config
from showbackup.utils import create_not_exists

LOG_DIR = "/var/log/showbackup"
LOG_FILENAME = "showbackup.log"
LOG_ERROR_FILENAME = "showbackup_error.log"

create_not_exists(LOG_DIR)

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(threadName)s:%(thread)d] [%(filename)s:%(lineno)d] [%(levelname)s]- %(message)s"
        }
    },
    "handlers": {
        "debug_console_handler": {
            "level": "DEBUG",
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",  # Default is stderr
        },
        "info_rotating_file_handler": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "INFO",
            "formatter": "standard",
            "filename": os.path.join(LOG_DIR, LOG_FILENAME),
            "when": "midnight",
            "interval": 1,
            "backupCount": 6,
            "encoding": "utf-8",
        },
        "error_file_handler": {
            "level": "WARNING",
            "formatter": "standard",
            "class": "logging.FileHandler",
            "filename": os.path.join(LOG_DIR, LOG_ERROR_FILENAME),
            "mode": "a",
            "encoding": "utf-8",
        },
    },
    "loggers": {
        "": {  # root logger,可以用作生产环境
            "handlers": [
                "debug_console_handler",
                "info_rotating_file_handler",
                "error_file_handler",
            ],
            "level": "INFO",
        },
        "__main__": {  # if __name__ == '__main__'
            "handlers": [
                "debug_console_handler",
                "info_rotating_file_handler",
                "error_file_handler",
            ],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}


def get_logger(name=None):
    logging.config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger(name)
    return logger
