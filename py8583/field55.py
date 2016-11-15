# coding=utf-8
import binascii
import json

def parse(s):
    """

    :param s:
    :type s: str
    :return:
    :rtype: dict
    """
    fields = {}

    index = 0
    while index < len(s):
        tag = s[index]
        # 判定tag是否占两个字节长度
        if 0b11111 == (ord(tag) & 0b11111):
            tag = s[index:index+2]
            index += 2
        else:
            index += 1
        tag = binascii.hexlify(tag)

        # 求长度
        length, length_len = _parse_len(s, index)
        index += length_len

        value = s[index:index+length]
        value = binascii.hexlify(value)
        index += length

        fields[tag] = {
            'len': length,
            'value': value
        }


    return fields

def build(data):
    """

    :param data:
    :type data: dict[str,dict]
    :return: hexlify str
    :rtype: str
    """

    fields = []
    for tag, info in data.items():
        field = tag + _build_len(info['len']) + info['value']

        fields.append(field)

    return ''.join(fields)

def _build_len(length):
    """

    :param length:
    :type length: int
    :return:
    :rtype: str
    """

    assert length >= 0 and length <= 65535

    if length <= 127:
        len_str = chr(length)
    elif 128 <= length and length <= 255:
        len_byte1 = chr(0x81)
        len_byte2 = chr(length)

        len_str = len_byte1+len_byte2
    else:
        len_byte1 = chr(0x82)
        len_byte2 = chr(length>>8)
        len_byte3 = chr(length&0xff)

        len_str = len_byte1+len_byte2+len_byte3

    return binascii.hexlify(len_str)

def _parse_len(s, index):
    length_byte1 = s[index]

    if 0 == (ord(length_byte1) & 0x80):  # 第一字节最高位为0, 长度为1字节
        length = ord(length_byte1)
        length_len = 1
    else:  # 第一字节最高位为1,T的长度为变长(第一字节右边7bit为T的长度)
        length_byte2 = s[index + 1]

        # 这是L的值 所占的字节. L的长度 所占字节固定为1
        remain_bytes = ord(length_byte1) & 0x7f
        assert remain_bytes == 1 or remain_bytes == 2
        length_len = 1 + remain_bytes

        if remain_bytes == 1:
            length = ord(length_byte2)
        else:  # remain_bytes == 2
            length_byte3 = s[index + 2]
            length = ord(length_byte2) << 8 + ord(length_byte3)

    return length, length_len


if __name__ == '__main__':
    
    s_l = [
        
    ]

    for s in s_l:
        print json.dumps(parse(s), indent=4)

