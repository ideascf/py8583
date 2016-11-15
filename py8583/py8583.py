# coding=utf-8
import binascii
import json
import logging
import struct

from . import constant
from . import err
from .field import Py8583Field
from .spec import Py8583Spec

log = logging.getLogger(constant.LOGGER_NAME)

class Py8583(object):
    _BIT_DEFAULT_VALUE = 0

    #### meta ####
    def __init__(self, spec):
        """

        :param spec:
        :type spec: Py8583Spec
        :return:
        """

        self.spec = spec

        self.bitmap = []
        self.all_field_data = {}
        self._MTI = ''  # message type identifier

        self.reset()

    def __str__(self):
        mti_info = 'MTI: %s' % self._MTI
        bitmap_info = 'bitmap: %s' % self.bitmap_info()
        all_field_innfo = self.field_info()

        return ''.join([mti_info, bitmap_info, all_field_innfo])

    def reset(self):
        self.all_field_data = {}
        self._MTI = ''
        self._reset_bitmap()

    #### property ####
    @property
    def MTI(self):
        return self._MTI

    @MTI.setter
    def MTI(self, MTI):
        try:  # MTI should only contain numbers
            int(MTI)
        except:
            raise ValueError("Invalid MTI [{0}]: MTI must contain only numbers".format(MTI))

        self._MTI = MTI

    #### field ####
    def get_field_spec(self, bit):
        """

        :param bit:
        :type bit: int | str
        :return:
        :rtype: Py8583Field
        """

        return self.spec[bit]

    def get_bit(self, bit):
        self._check_bit(bit)

        if not self.bitmap[bit]:
            raise err.Py8583BitNotExistError('bit(%s) not exist in bitmap.' % bit)
        else:
            return self.all_field_data[bit]

    def set_bit(self, bit, value):
        self._check_bit(bit)

        field_spec = self.get_field_spec(bit)

        self.all_field_data[bit] = value
        self._update_bitmap(bit, 1)

    def clear_bit(self, bit):
        self._check_bit(bit)

        self.all_field_data.pop(bit, None)  # delete data
        self._update_bitmap(bit, 0)

    #### build ####
    def build(self):
        """
        Build result str.
        :return:
        :rtype: str
        """
        result = b''.join(
            [
                self._build_MTI(),
                self._build_bitmap(),
                self._build_all_field(),
            ]
        )

        log.debug('MTI: %s', self.MTI)
        log.debug('Bitmap: %s', self.bitmap_info())
        log.debug('Field: \n%s', self.field_info())

        return result

    def _build_MTI(self):
        mti_spec = self.get_field_spec('MTI')

        return mti_spec.pack(self.MTI)

    def _build_bitmap(self):
        extended = self.bitmap[1]

        primary_bitmap = 0
        secondary_bitmap = 0
        for bit in range(1, 65):
            primary_bitmap |= self.bitmap[bit] << (64 - bit)
        for bit in range(65, 129):
            secondary_bitmap |= self.bitmap[bit] << (128 - bit)

        packed_bitmap = struct.pack('!Q', primary_bitmap)
        if extended:
            packed_bitmap += struct.pack('!Q', secondary_bitmap)

        bitmap_spec = self.get_field_spec(1)
        return bitmap_spec.pack(packed_bitmap)

    def _build_all_field(self):
        all_filed = [
            self._build_field(bit)
            for bit in range(2, 129)  # index startwith 1, and index 1 is extend bitmap flag.
            if self.bitmap[bit]
        ]

        return ''.join(all_filed)

    def _build_field(self, bit):
        if not self.bitmap[bit]:
            raise err.Py8583BitNotExistError('bit(%s) not exist in bitmap' % bit)

        field_spec = self.get_field_spec(bit)
        data = self.all_field_data[bit]
        log.debug(
            'build_field: %s, index(%s), data(%s), len(%s), content_type(%s), type(%s)',
            field_spec.field_name, bit, data, len(str(data)), field_spec.content_type, type(data)
        )

        return field_spec.pack(data)

    #### parse ####
    def parse(self, msg):
        pos = self._parse_MTI(msg, 0)
        log.debug('MTI: %s', self.MTI)

        pos = self._parse_bitmap(msg, pos)
        log.debug('Bitmap: %s', self.bitmap_info())

        pos = self._parse_all_field(msg, pos)
        log.debug('Field: \n%s', self.field_info())

    def _parse_MTI(self, msg, pos):
        mti_spec = self.get_field_spec('MTI')
        mti, data_len = mti_spec.unpack(msg, pos)
        self.MTI = mti

        return pos+data_len

    def _parse_bitmap(self, msg, pos):
        bitmap_spec = self.spec[1]

        data_type = bitmap_spec.data_type
        if data_type == constant.DataType.BIN:
            primary = msg[pos:pos + 8]
            pos += 8
        else:  # ASCII
            primary = binascii.unhexlify(msg[pos: pos + 16])
            pos += 16

        # 构建主位图
        int_primary = struct.unpack_from('!Q', primary)[0]
        for i in range(1, 65):
            self.bitmap[i] = (int_primary >> (64 - i)) & 0x1

        # 填充扩展位图
        if self._bitmap_len() == 128:  # 使用了扩展位图
            if data_type == constant.DataType.BIN:
                secondary = msg[pos:pos + 8]
                pos += 8
            else:
                secondary = msg[pos:pos + 16]
                pos += 16

            int_secondary = struct.unpack_from('!Q', secondary)[0]
            for i in range(1, 65):
                self.bitmap[i + 64] = (int_secondary >> (64 - i)) & 0x1

        return pos

    def _parse_all_field(self, msg, pos):
        for bit in range(2, 129):  # index startwith 1, and index 1 is extend bitmap flag.
            if self.bitmap[bit]:
                pos = self._parse_field(bit, msg, pos)

    def _parse_field(self, bit, msg, pos):
        field_spec = self.get_field_spec(bit)

        field_value, new_pos = field_spec.unpack(msg, pos)
        self.set_bit(bit, field_value)
        log.debug(
            'parse_field:  %s, index(%s), value(%s), len(%s), type(%s)',
            field_spec.field_name, bit, field_value, (new_pos-pos), type(field_value)
        )

        return new_pos

    #### helper ####
    def _check_bit(self, bit):
        if bit < 1 or bit > 128:
            raise err.Py8583ProgramError('Bit number %s out of range.' % bit)

    def _reset_bitmap(self):
        if len(self.bitmap) == 129:  # initialized
            for index in range(1, 129):  # index(0) is NOT used
                self.bitmap[index] = self._BIT_DEFAULT_VALUE
        else:  # first initialize
            for index in range(0, 129):  # index(0) is NOT used, but placehold
                self.bitmap.append(self._BIT_DEFAULT_VALUE)

    def _trans_value(self, field_spec):
        """

        :param field_spec:
        :type field_spec: Py8583Field
        :return:
        """

        value = self.all_field_data[field_spec.index]
        """:type: str"""
        data_type = field_spec.data_type

        try:
            ret = self.encode_data(value, data_type)
        except err.Py8583InvalidDataTypeError:
            raise err.Py8583InvalidDataTypeError('field_spec(%s) have invalid data_type(%s)' % field_spec, data_type)

        return ret

    def _bitmap_len(self):
        """
        返回位图的长度
        :return:
        """

        # bitmap[1] 标志是否使用扩展位图
        return 128 if self.bitmap[1] else 64

    def _update_bitmap(self, bit, flag):
        """

        :param bit:
        :param flag: 0 clear the <bit>, 1 set the <bit>
        :type flag: int
        :return:
        """

        if flag not in (0, 1):
            raise err.Py8583ProgramError('flag(%s) must be 0 or 1' % flag)

        self.bitmap[bit] = flag
        self._update_extend_bitmap_flag()

    def _update_extend_bitmap_flag(self):
        """
        Update the flag which determine whether or not use extend bitmap.
        :return:
        """

        if 1 in self.bitmap[65:]:  # 判定扩展位图是否有值
            self.bitmap[1] = 1  # enable extend bitmap
        else:
            self.bitmap[1] = 0  # diable extend bitmap

    #### show method ####
    def bitmap_info(self):
        """

        :return:
        :rtype: str
        """

        bitmap_str = json.dumps(self.bitmap, separators=(',', ':'))  # got '[1,0,1,0,1,0,0,1...]'
        bitmap_str = bitmap_str.strip('[]')  # remove '[' and ']', got '1,0,1,0,1,0,0,1...'
        bitmap_str = bitmap_str.replace(',', '')  # Got '100101001...'
        splitted_bitmap_str = ' | '.join(
            bitmap_str[i:i + 8]
            for i in range(1, self._bitmap_len() + 1, 8)  # split every 8 character
        )  # Got 10010100 | 1...

        return splitted_bitmap_str

    def field_info(self):
        all_field_info_list = []
        for index in sorted(self.all_field_data.keys()):
            field_data = self.all_field_data[index]
            field_spec = self.get_field_spec(index)

            if field_spec.content_type == 'n' and field_spec.data_len_type == constant.LengthType.FIXED:
                field_data = str(field_data).zfill(field_spec.data_len_max)

            all_field_info_list.append(
                u'\t{0:>3d} - {1: <41} : [{2}]'.format(index, field_spec.field_name, repr(field_data))
            )

        all_field_info = '\n'.join(all_field_info_list)

        return all_field_info


def bcd2str(bcd):
    return binascii.hexlify(bcd).decode('latin')


def str2bcd(string):
    if(len(string) % 2 == 1):
        string = string.zfill(len(string) + 1)
    return binascii.unhexlify(string)
