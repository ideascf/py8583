# coding=utf-8

from .field import Py8583Field
from .constant import DataType, LengthType

class Py8583Spec(object):
    _valid_content_types = ('a', 'n', 's', 'an', 'as', 'ns', 'ans', 'b', 'z')

    def __init__(self):
        self._spec = {
            1 : Py8583Field(1, 'Bit Map Extended', 'b', 8, LengthType.FIXED),
            2 : Py8583Field(2, 'Primary account number (PAN)', 'n', 19, LengthType.LLVAR),
            3 : Py8583Field(3, 'Precessing code', 'n', 6, LengthType.FIXED),
            4 : Py8583Field(4, 'Amount transaction', 'n', 12, LengthType.FIXED),
            5 : Py8583Field(5, 'Amount reconciliation', 'n', 12, LengthType.FIXED),
            6 : Py8583Field(6, 'Amount cardholder billing', 'n', 12, LengthType.FIXED),
            7 : Py8583Field(7, 'Date and time transmission', 'n', 10, LengthType.FIXED),
            8 : Py8583Field(8, 'Amount cardholder billing fee', 'n', 8, LengthType.FIXED),
            9 : Py8583Field(9, 'Conversion rate reconciliation', 'n', 8, LengthType.FIXED),
            10 : Py8583Field(10, 'Conversion rate cardholder billing', 'n', 8, LengthType.FIXED),
            #
            11 : Py8583Field(11, 'Systems trace audit number', 'n', 6, LengthType.FIXED),
            12 : Py8583Field(12, 'Date and time local transaction', 'n', 6, LengthType.FIXED),
            13 : Py8583Field(13, 'Date effective', 'n', 4, LengthType.FIXED),
            14 : Py8583Field(14, 'Date expiration', 'n', 4, LengthType.FIXED),
            15 : Py8583Field(15, 'Date settlement', 'n', 4, LengthType.FIXED),
            16 : Py8583Field(16, 'Date conversion', 'n', 4, LengthType.FIXED),
            17 : Py8583Field(17, 'Date capture', 'n', 4, LengthType.FIXED),
            18 : Py8583Field(18, 'Message error indicator', 'n', 4, LengthType.FIXED),
            19 : Py8583Field(19, 'Country code acquiring institution', 'n', 3, LengthType.FIXED),
            20 : Py8583Field(20, 'Country code primary account number (PAN)', 'n', 3, LengthType.FIXED),
            #
            21 : Py8583Field(21, 'Transaction life cycle identification data', 'n', 3, LengthType.FIXED),
            22 : Py8583Field(22, 'Point of service data code', 'n', 3, LengthType.FIXED),
            23 : Py8583Field(23, 'Card sequence number', 'n', 3, LengthType.FIXED),
            24 : Py8583Field(24, 'Function code', 'n', 3, LengthType.FIXED),
            25 : Py8583Field(25, 'Message reason code', 'n', 2, LengthType.FIXED),
            26 : Py8583Field(26, 'Merchant category code', 'n', 2, LengthType.FIXED),
            27 : Py8583Field(27, 'Point of service capability', 'n', 1, LengthType.FIXED),
            28 : Py8583Field(28, 'Date reconciliation', 'an', 9, LengthType.FIXED),
            29 : Py8583Field(29, 'Reconciliation indicator', 'an', 9, LengthType.FIXED),
            30 : Py8583Field(30, 'Amounts original', 'an', 9, LengthType.FIXED),
            #
            31 : Py8583Field(31, 'Acquirer reference number', 'an', 9, LengthType.FIXED),
            32 : Py8583Field(32, 'Acquiring institution identification code', 'n', 11, LengthType.LLVAR),
            33 : Py8583Field(33, 'Forwarding institution identification code', 'n', 11, LengthType.LLVAR),
            34 : Py8583Field(34, 'Electronic commerce data', 'ns', 28, LengthType.LLVAR),
            35 : Py8583Field(35, 'Track 2 data', 'z', 37, LengthType.LLVAR),
            36 : Py8583Field(36, 'Track 3 data', 'n', 104, LengthType.LLLVAR),
            37 : Py8583Field(37, 'Retrieval reference number', 'an', 12, LengthType.FIXED),
            38 : Py8583Field(38, 'Approval code', 'an', 6, LengthType.FIXED),
            39 : Py8583Field(39, 'Action code', 'an', 2, LengthType.FIXED),
            40 : Py8583Field(40, 'Service code', 'an', 3, LengthType.FIXED),
            #
            41 : Py8583Field(41, 'Card acceptor terminal identification', 'ans', 8, LengthType.FIXED),
            42 : Py8583Field(42, 'Card acceptor identification code', 'ans', 15, LengthType.FIXED),
            43 : Py8583Field(43, 'Card acceptor name/location', 'ans', 40, LengthType.FIXED),
            44 : Py8583Field(44, 'Additional response data', 'an', 25, LengthType.LLVAR),
            45 : Py8583Field(45, 'Track 1 data', 'an', 76, LengthType.LLVAR),
            46 : Py8583Field(46, 'Amounts fees', 'an', 999, LengthType.LLLVAR),
            47 : Py8583Field(47, 'Additional data national', 'an', 999, LengthType.LLLVAR),
            48 : Py8583Field(48, 'Additional data private', 'an', 999, LengthType.LLLVAR),
            49 : Py8583Field(49, 'Verification data', 'an', 3, LengthType.FIXED),
            50 : Py8583Field(50, 'Currency code, settlement', 'an', 3, LengthType.FIXED),
            #
            51 : Py8583Field(51, 'Currency code, cardholder billing', 'an', 3, LengthType.FIXED),
            52 : Py8583Field(52, 'Personal identification number (PIN) data', 'b', 8, LengthType.FIXED),
            53 : Py8583Field(53, 'Security related control information', 'n', 16, LengthType.FIXED),
            54 : Py8583Field(54, 'Amounts additional', 'an', 120, LengthType.LLLVAR),
            55 : Py8583Field(55, 'Integrated circuit card (ICC) system related data', 'ans', 999, LengthType.LLLVAR),
            56 : Py8583Field(56, 'Original data elements', 'ans', 999, LengthType.LLLVAR),
            57 : Py8583Field(57, 'Authorisation life cycle code', 'ans', 999, LengthType.LLLVAR),
            58 : Py8583Field(58, 'Authorising agent institution identification code', 'ans', 999, LengthType.LLLVAR),
            59 : Py8583Field(59, 'Transport data', 'ans', 999, LengthType.LLLVAR),
            60 : Py8583Field(60, 'Reserved for national use', 'ans', 999, LengthType.LLLVAR),
            #
            61 : Py8583Field(61, 'Reserved for national use', 'ans', 999, LengthType.LLLVAR),
            62 : Py8583Field(62, 'Reserved for private use', 'ans', 999, LengthType.LLLVAR),
            63 : Py8583Field(63, 'Reserved for private use', 'ans', 999, LengthType.LLLVAR),
            64 : Py8583Field(64, 'Message authentication code (MAC) field', 'b', 8, LengthType.FIXED),
            65 : Py8583Field(65, 'Bitmap tertiary', 'b', 1, LengthType.FIXED),
            66 : Py8583Field(66, 'Settlement code', 'n', 1, LengthType.FIXED),
            67 : Py8583Field(67, 'Extended payment data', 'n', 2, LengthType.FIXED),
            68 : Py8583Field(68, 'Receiving institution country code', 'n', 3, LengthType.FIXED),
            69 : Py8583Field(69, 'Settlement institution county code', 'n', 3, LengthType.FIXED),
            70 : Py8583Field(70, 'Network management Information code', 'n', 3, LengthType.FIXED),
            #
            71 : Py8583Field(71, 'Message number', 'n', 4, LengthType.FIXED),
            72 : Py8583Field(72, 'Data record', 'n', 4, LengthType.FIXED),
            73 : Py8583Field(73, 'Date action', 'n', 6, LengthType.FIXED),
            74 : Py8583Field(74, 'Credits, number', 'n', 10, LengthType.FIXED),
            75 : Py8583Field(75, 'Credits, reversal number', 'n', 10, LengthType.FIXED),
            76 : Py8583Field(76, 'Debits, number', 'n', 10, LengthType.FIXED),
            77 : Py8583Field(77, 'Debits, reversal number', 'n', 10, LengthType.FIXED),
            78 : Py8583Field(78, 'Transfer number', 'n', 10, LengthType.FIXED),
            79 : Py8583Field(79, 'Transfer, reversal number', 'n', 10, LengthType.FIXED),
            80 : Py8583Field(80, 'Inquiries number', 'n', 10, LengthType.FIXED),
            #
            81 : Py8583Field(81, 'Authorizations, number', 'n', 10, LengthType.FIXED),
            82 : Py8583Field(82, 'Credits, processing fee amount', 'n', 12, LengthType.FIXED),
            83 : Py8583Field(83, 'Credits, transaction fee amount', 'n', 12, LengthType.FIXED),
            84 : Py8583Field(84, 'Debits, processing fee amount', 'n', 12, LengthType.FIXED),
            85 : Py8583Field(85, 'Debits, transaction fee amount', 'n', 12, LengthType.FIXED),
            86 : Py8583Field(86, 'Credits, amount', 'n', 16, LengthType.FIXED),
            87 : Py8583Field(87, 'Credits, reversal amount', 'n', 16, LengthType.FIXED),
            88 : Py8583Field(88, 'Debits, amount', 'n', 16, LengthType.FIXED),
            89 : Py8583Field(89, 'Debits, reversal amount', 'n', 16, LengthType.FIXED),
            90 : Py8583Field(90, 'Original data elements', 'n', 42, LengthType.FIXED),
            #
            91 : Py8583Field(91, 'File update code', 'an', 1, LengthType.FIXED),
            92 : Py8583Field(92, 'File security code', 'an', 2, LengthType.FIXED),
            93 : Py8583Field(93, 'Response indicator', 'an', 5, LengthType.FIXED),
            94 : Py8583Field(94, 'Service indicator', 'an', 7, LengthType.FIXED),
            95 : Py8583Field(95, 'Replacement amounts', 'an', 42, LengthType.FIXED),
            96 : Py8583Field(96, 'Message security code', 'b', 8, LengthType.FIXED),
            97 : Py8583Field(97, 'Amount, net settlement', 'an', 16, LengthType.FIXED),
            98 : Py8583Field(98, 'Payee', 'ans', 25, LengthType.FIXED),
            99 : Py8583Field(99, 'Settlement institution identification code', 'n', 11, LengthType.LLVAR),
            100 : Py8583Field(100, 'Receiving institution identification code', 'n', 11, LengthType.LLVAR),
            #
            101 : Py8583Field(101, 'File name', 'ans', 17, LengthType.LLVAR),
            102 : Py8583Field(102, 'Account identification 1', 'ans', 28, LengthType.LLVAR),
            103 : Py8583Field(103, 'Account identification 2', 'ans', 28, LengthType.LLVAR),
            104 : Py8583Field(104, 'Transaction description', 'ans', 100, LengthType.LLLVAR),
            105 : Py8583Field(105, 'Reserved for ISO use', 'ans', 999, LengthType.LLLVAR),
            106 : Py8583Field(106, 'Reserved for ISO use', 'ans', 999, LengthType.LLLVAR),
            107 : Py8583Field(107, 'Reserved for ISO use', 'ans', 999, LengthType.LLLVAR),
            108 : Py8583Field(108, 'Reserved for ISO use', 'ans', 999, LengthType.LLLVAR),
            109 : Py8583Field(109, 'Reserved for ISO use', 'ans', 999, LengthType.LLLVAR),
            110 : Py8583Field(110, 'Reserved for ISO use', 'ans', 999, LengthType.LLLVAR),
            #
            111 : Py8583Field(111, 'Reserved for private use', 'ans', 999, LengthType.LLLVAR),
            112 : Py8583Field(112, 'Reserved for private use', 'ans', 999, LengthType.LLLVAR),
            113 : Py8583Field(113, 'Reserved for private use', 'n', 11, LengthType.LLVAR),
            114 : Py8583Field(114, 'Reserved for national use', 'ans', 999, LengthType.LLLVAR),
            115 : Py8583Field(115, 'Reserved for national use', 'ans', 999, LengthType.LLLVAR),
            116 : Py8583Field(116, 'Reserved for national use', 'ans', 999, LengthType.LLLVAR),
            117 : Py8583Field(117, 'Reserved for national use', 'ans', 999, LengthType.LLLVAR),
            118 : Py8583Field(118, 'Reserved for national use', 'ans', 999, LengthType.LLLVAR),
            119 : Py8583Field(119, 'Reserved for national use', 'ans', 999, LengthType.LLLVAR),
            120 : Py8583Field(120, 'Reserved for private use', 'ans', 999, LengthType.LLLVAR),
            #
            121 : Py8583Field(121, 'Reserved for private use', 'ans', 999, LengthType.LLLVAR),
            122 : Py8583Field(122, 'Reserved for national use', 'ans', 999, LengthType.LLLVAR),
            123 : Py8583Field(123, 'Reserved for private use', 'ans', 999, LengthType.LLLVAR),
            124 : Py8583Field(124, 'Info Text', 'ans', 255, LengthType.LLLVAR),
            125 : Py8583Field(125, 'Network management information', 'ans', 50, LengthType.LLVAR),
            126 : Py8583Field(126, 'Issuer trace id', 'ans', 6, LengthType.LLVAR),
            127 : Py8583Field(127, 'Reserved for private use', 'ans', 999, LengthType.LLLVAR),
            128 : Py8583Field(128, 'Message authentication code (MAC) field', 'b', 16, LengthType.FIXED),
        }

    def __getitem__(self, item):
        """

        :param item:
        :return:
        :rtype: Py8583Field
        """

        return self._spec[item]

