# coding=utf-8
"""

"""
import json
import binascii
import logging

from . import constant
from . import err


log = logging.getLogger(constant.LOGGER_NAME)


class Py8583Field(object):
    _FORMAT_STR = '{index}'
    def __init__(self, index, field_name, content_type, data_len_max, data_len_type, encoding='latin', remark=''):
        """
        value -> content -> data -> field

        data = content_len(可空) + content
        content: 存放该域的值(value), 可能会对value做些封装, 比如: 根据content_type对value做padding

        :param index: 域, 第几域
        :param field_name: 该域的名称, 如 'Primary account number (PAN)'
        :param content_type: 该域的值的类型, 可以是: 字母字符串, 数字字符串, 二进制串, 月份(MM), 日期(DD)等
        :param data_len_max: 将该域的值(content)打包为data后, data的最大长度
        :param data_len_type: data的长度类型, 定长, 1位变长, 2位变长, 3位变长
        :param data_type: 封装该域的值(content) 的容器的类型,可以是二进制,ASC字符串,BCD码
        :param encoding: content的编码, 如utf8, latin. 需要将value编码为encoding指定的编码方式.
        :param remark: 备注
        """
        self.index = index  # 域索引

        self.field_type = None  # 域名类型
        self.field_name = field_name  # 域名

        self.data_len_max = data_len_max  # 数据长度最大值
        self.data_len_type = data_len_type  # 数据长度类型
        self.data_len_encode_type = constant.DataType.ASCII  # 数据域长度的编码类型

        self.data_type = self._gen_data_type(content_type)  # 数据类型
        self.content_type = content_type
        self.reserved = None  # 保留

        self.remark = remark
        self.encoding = encoding

    def __str__(self):
        return json.dumps(
            vars(self),
            indent=4
        )

    def gen_data_len(self, data):
        """
        通过content, 计算得到data_len
        :param data:
        :type data: str
        :return:
        :rtype: str | None
        """

        if self.data_len_type == constant.LengthType.FIXED:
            data_len_final = None
        else:
            data_len = len(data)
            if data_len > self.data_len_max:
                raise err.Py8583DataTooLongError(
                    'field(%s) Got content_len(%s) > max(%s), data(%s)'
                    % (self, data_len, self.data_len_max, data)
                )

            if self.data_len_type == constant.LengthType.LVAR:
                data_len_str = "{0:01d}".format(data_len)
            elif self.data_len_type == constant.LengthType.LLVAR:
                data_len_str = "{0:02d}".format(data_len)
            elif self.data_len_type == constant.LengthType.LLLVAR:
                data_len_str = "{0:03d}".format(data_len)
            else:
                raise err.Py8583ProgramError('field(%s) have invalid len_type(%s)' % (self, self.data_len_type))

            data_len_final = self.encode_data(data_len_str, self.data_len_encode_type)

        log.debug('pack field(%s), data_len_final(%s)', self.index, data_len_final)
        return data_len_final

    def get_data_len(self, msg, pos):
        """

        :param msg:
        :type msg: str
        :param pos:
        :type pos: int
        :return: data_len
        :rtype: int
        """

        data_len_type = self.data_len_type
        data_len_encode_type = self.data_len_encode_type
        data_len_max = self.data_len_max

        if data_len_type == constant.LengthType.FIXED:
            data_len = data_len_max
        elif data_len_type == constant.LengthType.LVAR:
            data_len = int(self.decode_data(msg[pos:pos + 1], data_len_encode_type))
            pos += 1
        elif data_len_type == constant.LengthType.LLVAR:
            data_len = int(self.decode_data(msg[pos:pos + 2], data_len_encode_type))
            pos += 2
        elif data_len_type == constant.LengthType.LLLVAR:
            data_len = int(self.decode_data(msg[pos:pos + 3], data_len_encode_type))
            pos += 3
        else:
            raise err.Py8583ProgramError('Field({}) have invalid data_len_type({})'.format(self, data_len_type))

        if data_len > data_len_max:
            raise ValueError('unpack field(%s) failed, data_len(%s) is too long > max(%s)' % (self, data_len, data_len_max))

        log.debug('unpack field(%s), data_len(%s)', self.index, data_len)
        return data_len, pos

    def encode_content(self, value):
        """
        封装value得到content
        :param value:
        :type value: object
        :return: content
        :rtype: str
        """

        len_type = self.data_len_type
        data_len_max = self.data_len_max
        content_type = self.content_type

        if len_type == constant.LengthType.FIXED:
            if content_type == 'n':
                formatter = '{{0:0>{len}}}'.format(len=data_len_max)  # if len is 3, formatter is '{0:03d}'
            elif any(t in content_type for t in 'ans'):  # any of 'ans' in content_type
                formatter = '{{0: >{0}}}'.format(data_len_max)  # if len is 3, formatter is '{0: >3}'
            else:
                formatter = '{0}'

            content = formatter.format(value)
        else:
            content = str(value)

        # 处理磁道信息
        content = self._trans_track_data(content)

        return content

    def decode_content(self, content):
        """

        :param content:
        :type content: str
        :return: value
        :rtype: object
        """

        content_type = self.content_type

        if content_type == 'n':
            # value = int(content)
            value = content
        else:
            value = content

        # 处理磁道信息
        value = self._untrans_track_data(value)

        return value

    def encode_data(self, content, data_type):
        """
        将content打包为data.
        pack content into data.
        :param content:
        :param data_type:
        :type content: str
        :type data_type: int
        :return: data
        :rtype: str
        """

        if data_type == constant.DataType.ASCII:
            data = content
        elif data_type == constant.DataType.BCD:
            data = str2bcd(content)
        elif data_type == constant.DataType.BIN:
            data = content
        else:
            raise err.Py8583InvalidDataTypeError('data_type(%s) is invalid.' % data_type)

        return data

    def decode_data(self, data, data_type):
        """

        :param data:
        :param data_type:
        :type data: str
        :type data_type: int
        :return: content
        :rtype: str
        """

        if data_type == constant.DataType.ASCII:
            content = data
        elif data_type == constant.DataType.BCD:
            content = bcd2str(data)
        elif data_type == constant.DataType.BIN:
            content = data
        else:
            raise err.Py8583InvalidDataTypeError('data_type(%s) is invalid.' % data_type)

        return content

    def pack(self, data):
        raise NotImplementedError()

    def unpack(self, msg, pos=0):
        raise NotImplementedError()

    # helper
    def _gen_data_type(self, content_type):
        if content_type == 'b':
            return constant.DataType.BIN
        else:
            return constant.DataType.ASCII

    def _trans_track_data(self, value):
        # 处理磁道信息
        if self.content_type == 'z':
            value = value.replace('=', 'D')
            if(len(value) % 2 == 1):
                value = value + 'F'

        return value

    def _untrans_track_data(self, value):
        """

        :param value:
        :type value: str
        :return:
        """

        # 处理磁道信息
        if self.content_type == 'z':
            value = value.replace('D', '=')  # in track2, replace 'D' with '='
            value = value.rstrip('F')  # in track2, remove trailing 'F'

        return value


class Py8583SimpleField(Py8583Field):
    def pack(self, value):
        """

        :param value:
        :type value: object
        :return:
        :rtype: str
        """

        content = self.encode_content(value)
        data = self.encode_data(content, self.data_type)
        data_len = self.gen_data_len(data)

        if data_len is None:  # fixed length
            return data
        else:
            return data_len + data

    def unpack(self, msg, pos=0):
        """

        :param msg:
        :type msg: str
        :param pos:
        :type pos: int
        :return:
        :rtype: object
        """

        data_len, pos = self.get_data_len(msg, pos)
        content = self.decode_data(msg[pos: pos+data_len], self.data_type)
        value = self.decode_content(content)

        return value, pos+data_len


class Py8583ComposedField(Py8583Field):
    def pack(self, data):
        raise NotImplementedError()

    def unpack(self, msg, pos=0):
        raise NotImplementedError()


def bcd2str(bcd):
    return binascii.hexlify(bcd).decode('latin')


def str2bcd(string):
    if(len(string) % 2 == 1):
        string = string.zfill(len(string) + 1)
    return binascii.unhexlify(string)
