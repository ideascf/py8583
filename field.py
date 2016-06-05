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

    def encode_content_len(self, content):
        if self.data_len_type == constant.LengthType.FIXED:
            len_data = None
        else:
            content_len = len(content)
            if content_len > self.data_len_max:
                raise err.Py8583DataTooLongError(
                    'field(%s) Got content_len(%s) > max(%s), content(%s)'
                    % (self, content_len, self.data_len_max, content)
                )

            if self.data_len_type == constant.LengthType.LVAR:
                len_data = "{0:01d}".format(content_len)
            elif self.data_len_type == constant.LengthType.LLVAR:
                len_data = "{0:02d}".format(content_len)
            elif self.data_len_type == constant.LengthType.LLLVAR:
                len_data = "{0:03d}".format(content_len)
            else:
                raise err.Py8583ProgramError('field(%s) have invalid len_type(%s)' % (self, self.data_len_type))

            len_data = self.encode_data(len_data, self.data_len_encode_type)

        return len_data

    def decode_content_len(self, msg, pos):
        content_len = 0
        data_type = self.data_type
        data_len_type = self.data_len_type
        data_len_encode_type = self.data_len_encode_type
        content_type = self.content_type
        data_len_max = self.data_len_max

        if data_type == constant.DataType.ASCII and content_type == 'b':
            data_len_max *= 2

        if data_len_type == constant.LengthType.FIXED:
            content_len = data_len_max
        elif data_len_type == constant.LengthType.LVAR:
            pass
        elif data_len_type == constant.LengthType.LLVAR:
            if data_len_encode_type == constant.DataType.ASCII:
                content_len = int(self.decode_data(msg[pos:pos + 2], data_len_encode_type))
                pos += 2
            elif data_len_encode_type == constant.DataType.BCD:  # BCD
                content_len = int(self.decode_data(msg[pos:pos + 1], data_len_encode_type))
                pos += 1
            else:
                raise err.Py8583InvalidDataTypeError('unpack field(%s) got invalid data_len_encode_type' % self)
        elif data_len_type == constant.LengthType.LLLVAR:
            if data_len_encode_type == constant.DataType.ASCII:
                content_len = int(self.decode_data(msg[pos:pos + 3], data_len_encode_type))
                pos += 3
            elif data_len_encode_type == constant.DataType.BCD:  # BCD
                content_len = int(self.decode_data(msg[pos:pos + 2], data_len_encode_type))
                pos += 2
            else:
                raise err.Py8583InvalidDataTypeError('unpack field(%s) got invalid data_len_encode_type' % self)

        if content_len > data_len_max:
            raise ValueError('unpack field(%s) failed, data_len(%s) is too long > max(%s)' % (self, content_len, data_len_max))
        if content_len == 0:
            return ValueError('unpack field(%s) failed, data_len(%s) is 0' % (self, content_len))


        return content_len, pos

    def encode_content(self, value):
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

            value = formatter.format(value)
        else:
            value = str(value)

        # 处理磁道信息
        value = self._trans_track_data(value)

        return value

    def decode_content(self, content):
        content_type = self.content_type

        if content_type == 'n':
            # value = int(content)
            value = content
        else:
            value = content

        # 处理磁道信息
        value = self._untrans_track_data(value)

        return value

    def encode_data(self, data, data_type):
        if data_type == constant.DataType.ASCII:
            # ret = data.encode(self.encoding)
            ret = data
        elif data_type == constant.DataType.BCD:
            ret = str2bcd(data)
        elif data_type == constant.DataType.BIN:
            ret = data
        else:
            raise err.Py8583InvalidDataTypeError('data_type(%s) is invalid.' % data_type)

        return ret

    def decode_data(self, data, data_type):
        """


        :param content_type:
        :param data:
        :param data_type:
        :type data: str
        :return:
        """

        if data_type == constant.DataType.ASCII:
            # ret = data.decode(self.encoding)
            ret = data
        elif data_type == constant.DataType.BCD:
            ret = bcd2str(data)
        elif data_type == constant.DataType.BIN:
            ret = data
        else:
            raise err.Py8583InvalidDataTypeError('data_type(%s) is invalid.' % data_type)

        return ret

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
        content = self.encode_content(value)
        cotent_len = self.encode_content_len(content)
        data = self.encode_data(content, self.data_type)

        if cotent_len is None:
            return data
        else:
            return cotent_len + data

    def unpack(self, msg, pos=0):
        data_type = self.data_type

        content_len, pos = self.decode_content_len(msg, pos)
        if data_type == constant.DataType.ASCII:
            data_len = content_len
        elif data_type == constant.DataType.BCD:
            data_len = (content_len+1)//2
        else:
            data_len = content_len

        content = self.decode_data(msg[pos: pos+data_len], data_type)
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
