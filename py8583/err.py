# coding=utf-8

class Py8583Error(Exception):
    pass

class Py8583ProgramError(Py8583Error):
    """
    program error.
    """
    pass


class Py8583BitNotExistError(Py8583Error):
    """
    Bit not in bitmap.
    """
    pass


class Py8583DataTooLongError(Py8583Error):
    """
    len of data is too long.
    """
    pass


class Py8583InvalidDataTypeError(Py8583Error):
    """
    Invalid data type.
    """
    pass