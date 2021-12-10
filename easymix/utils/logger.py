#! /usr/bin/env python
# -*-coding=utf8-*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import datetime
import logging
import os
import threading
import time


logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)

_init = False
_logfile = ''

loglevel_map = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warn': logging.WARN,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'fatal': logging.FATAL,
}


def set_logfile(logfile):
    global _logfile
    _logfile = logfile


def set_loglevel(loglevel):
    global logger, loglevel_map
    loglevel = loglevel.lower()
    if loglevel not in loglevel_map:
        raise ValueError("loglevel '{}' unknown".format(loglevel))
    logger.setLevel(loglevel_map[loglevel])


def start():
    th = threading.Thread(target=init_log, args=());
    th.start()
    time.sleep(1)


def init_log():
    global logger
    while True:
        year = str(datetime.datetime.now().year)
        month = '{0:02d}'.format(datetime.datetime.now().month)
        day = '{0:02d}'.format(datetime.datetime.now().day)
        time_day = year + month + day
        log_file_path = _logfile + '.' + time_day
        if not os.path.exists(log_file_path):
            os.system("touch " + log_file_path)
        handler = logging.FileHandler(log_file_path)
        formatter = logging.Formatter(
            "[%(levelname)s] %(asctime)s %(process)d "
            "%(filename)s:%(lineno)d] %(message)s")
        handler.setFormatter(formatter)
        logger.handlers = []
        logger.addHandler(handler)
        time.sleep(60)


if __name__ == '__main__':
    set_logfile('test.log')
    init_log()
    logger.info("test info logger")
    init_log()
    logger.error("test error logger")
