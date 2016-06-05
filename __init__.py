# coding=utf-8
import logging

from .constant import LOGGER_NAME


log = logging.getLogger(LOGGER_NAME)
log.propagate = 0  # 不要扩散到parent