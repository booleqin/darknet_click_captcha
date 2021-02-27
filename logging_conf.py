# -*-coding:utf-8-*- 
"""
日志改写
created by boole @ 2021-02-27
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging.config

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': "%(asctime)s | %(levelname)s | %(lineno)d | %(module)s | %(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'cloghandler.ConcurrentRotatingFileHandler',
            # 当达到1GB时分割日志
            'maxBytes': 1024 * 1024 * 1024 * 1,
            # 最多保留10份文件
            'backupCount': 10,
            # If delay is true,
            # then file opening is deferred until the first call to emit().
            'delay': True,
            'filename': './log/output.log',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        '': {
            'handlers': ['file'],
            'level': 'INFO',
        },
    }
})

logger = logging.getLogger(__name__)

