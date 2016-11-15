# coding=utf-8
from enum import IntEnum

class DataType(IntEnum):
    BCD = 1
    ASCII = 2
    BIN = 3

class LengthType(IntEnum):
    FIXED = 0
    LVAR = 1
    LLVAR = 2
    LLLVAR = 3

# logging模块的logger名称
# LOGGER_NAME = 'py8583'
LOGGER_NAME = None