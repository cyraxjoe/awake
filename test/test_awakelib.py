# -*- coding: utf-8 -*-
import os
import sys
import unittest
import string
import socket
import random

from awake import utils, wol

import _test_utils

INVALID_BROADCASTS = ['0.1.1.1.1',
                      '0.2.3.4.5',
                      '255.255.255.256',
                      '1.5.2.300']



class TestMACFormat(unittest.TestCase):

    def test_invalid_hexnumber(self):
        test_mac = 'ff:gg:11:11:11:00'
        self.assertRaises(ValueError,
                          utils.retrive_MAC_digits,
                          test_mac)


    def test_too_long(self):
        test_mac = 'ff:ff:11:11:11:00:ff'
        self.assertRaises(ValueError,
                          utils.retrive_MAC_digits,
                          test_mac)


    def test_too_short(self):
        test_mac = 'ff:FF:11:11:11'
        self.assertRaises(ValueError,
                          utils.retrive_MAC_digits,
                          test_mac)


    def test_junk_bytes(self):
        test_mac = os.urandom(40)
        self.assertRaises(ValueError,
                          utils.retrive_MAC_digits,
                          test_mac)


    def test_lowercase(self):
        test_mac = 'ff:ff:ff:ff:ff:ff'
        hexdigits = utils.retrive_MAC_digits(test_mac)
        self.assertEqual(hexdigits, ['ff'] * 6)

        
    def test_uppercase(self):
        test_mac = 'FF:FF:FF:FF:FF:FF'
        hexdigits = utils.retrive_MAC_digits(test_mac)
        self.assertEqual(hexdigits, ['FF'] * 6)
        

    def test_no_separator(self):
        test_mac = '111111111111'
        hexdigits = utils.retrive_MAC_digits(test_mac)
        self.assertEqual(hexdigits, ['11'] * 6)


    def _test_chars(self, chars):
        sample_mac =  ['11'] * 6
        for separator in chars:
            test_mac = separator.join(sample_mac)
            hexdigits = utils.retrive_MAC_digits(test_mac)
            self.assertEqual(hexdigits, sample_mac)


    def test_ascii_chars_as_separator(self):
        self._test_chars(string.ascii_letters)
        

    def test_non_ascii_chars_as_separator(self):
        uchars = ['ñ', 'ಠ', '¡', '¿',
                  'ਦ', '◓', '᭜', '⒲',
                  'ꍿ', 'ꡲ', '⬬', 'ﻷ',
                  'ꆔ', 'ﭼ', 'Š', '𝚡','㌂']
        self._test_chars(uchars)
        
        
class TestUtils(unittest.TestCase):
    """Test the function of the module awake.utils except retrive_MAC_digits
    which is tested in TestMACFormat.
    """

    __test_py2_fetch_last_exception = """
    def __test_fetch_last_exception():
        message = 'Test Message'
        try:
            raise Exception(message)
        except Exception, exep:
            utilexep = utils.fetch_last_exception()
            self.assertEqual(utilexep, exep)""".strip()

    __test_py3_fetch_last_exception = """
    def __test_fetch_last_exception():
        message = 'Test Message'
        try:
            raise Exception(message)
        except Exception as exep:
            utilexep = utils.fetch_last_exception()
            self.assertEqual(utilexep, exep)""".strip()

    def test_fetch_last_exception(self):
        """Notice the hackish approach of using `eval`!, because of the valid
        reason (in my opinion) of version incompatibility on how the
        exception object get referenced in the except clause and validate according
        to the python version and avoid the SyntaxError.
        """
        def  __test_fetch_last_exception():
            raise Exception('This function need to be redefined '
                            'to the right version.')        
        if sys.version_info[0] == 2:
            testcode = compile(self.__test_py2_fetch_last_exception,
                               __name__, "exec")
        elif sys.version_info[0] == 3:
            testcode = compile(self.__test_py3_fetch_last_exception,
                               __name__, "exec")
        else:
            raise Exception('This python version is not supported.')
        env = {'self': self, 'utils': utils}
        env['__test_fetch_last_exception'] = __test_fetch_last_exception        
        eval(testcode, env)
        env['__test_fetch_last_exception']()

    
    def test__split_file(self):
        separators = ['|', '%', '!', '*', ':', ',', '\n']
        for separator in separators:
            lines = []
            for letter in string.ascii_letters:
                line = letter * 10
                lines.append(line)
            fpath = _test_utils.create_sample_file(separator.join(lines))
            try:
                self.assertEqual(utils._split_file(fpath, separator),
                                 lines)
            finally:
                os.remove(fpath)


    def test__is_hexnumber(self):
        invalid_objects = (3.1416, complex(1,45), object(),
                           False, True, [], (), {}, set(),
                           frozenset(), 123)
        valid_hexdigits = [str(n)  for n in range(11)] + ['A', 'B', 'C',
                                                          'D', 'E', 'F']
        invalid_hexdigits = list(string.ascii_lowercase[6:])
        iterations = 50000
        for i in range(iterations):
            random.shuffle(valid_hexdigits)
            random.shuffle(invalid_hexdigits)
            valid_number = ''.join(valid_hexdigits)
            invalid_number = ''.join(valid_hexdigits + invalid_hexdigits)
            self.assertIs(utils._is_hexnumber(valid_number), True)
            self.assertIs(utils._is_hexnumber(invalid_number), False)
        for invalid_obj in invalid_objects:
            self.assertIs(utils._is_hexnumber(invalid_obj), False,
                          'The object %r evaluate to True.' % (invalid_obj,))



    def test__strip_separator_from_mac(self):
        # the validity or invalidity is just based in the lenght not
        # in the characters.
        valid_mac_pairs = [('1' * 12, '1' * 12),
                           ('a' * 12, 'a' * 12),
                           ('A1' * 6, 'A1' * 6),
                           (':'.join(['FF',] * 6), 'FF' * 6),
                           (';'.join(['3B',] * 6), '3B' * 6),
                           ('%'.join(['23',] * 6), '23' * 6)]
        invalid_macs = ['12', '1'* 13, '3b' * 7,
                        ':'.join(['FF',] * 7),
                        '|'.join(['FF',] * 3),
                        '@'.join(['FF',] * 20)]
        for pre_mac, post_mac in valid_mac_pairs:
            self.assertEqual(utils._strip_separator_from_mac(pre_mac),
                             post_mac)
        for invalid_mac in invalid_macs:
            self.assertRaises(ValueError, utils._strip_separator_from_mac, invalid_mac)

        
    def test_is_valid_broadcast_ip(self):
        valid_broadcasts = ['255.255.255.255',
                            '1.1.1.1.255',
                            '192.168.2.42',
                            '172.255.255.255',]
        for address in INVALID_BROADCASTS:
            self.assertIs(utils.is_valid_broadcast_ip(address), False)
        for address in valid_broadcasts:
            self.assertIs(utils.is_valid_broadcast_ip(address), True)
                

    def test_fetch_macs_from_file(self):
        
        slines = ['11.11.11.11.11 # one',
                  '22.11.11.11.11 # two',
                  'Invalid mac # thats ok',
                  '# line with comment']
        
        expmacs = ['11.11.11.11.11',
                   '22.11.11.11.11',
                   'Invalid mac']
        separators = [':', '*', '!', '\n']
        for sep in separators:
            sfile = _test_utils.create_sample_file(sep.join(slines))
            try:
                for mac in utils.fetch_macs_from_file(sfile, '\n'):
                    self.assertIn(mac, expmacs)
            finally:
                os.remove(sfile)
    


class TestWOL(unittest.TestCase):

    def setUp(self):
        self.sample_mac = '1c:6f:66:31:e2:5f'


    def test_invalid_mac(self):
        macs = ['12:da:as:12:11:22',
                '12:da:as:12:11:22',
                '12daas121122',
                '12daaf12112',
                'fffffffffffff', # 13 digits
                'ff:ff:ff:ff@ff',
                '11;11;11;11;4G',
                111111111111,
                1, '']
        for mac in macs:
            self.assertRaises(ValueError, wol.send_magic_packet, mac)


    def test_invalid_broadcast(self):
        for bc in INVALID_BROADCASTS:
            try:
                wol.send_magic_packet('11:11:11:11:11:11', bc)
            except ValueError:
                e = utils.fetch_last_exception()
                self.assertIn('Invalid broadcast', e.args[0])
            else:
                emsg = "The broadcast '%s' should not pass the test! " % bc
                raise AssertionError(emsg)
            

    def test_invalid_dest(self):
        invalid_dest = ['192.168.0.256',
                        '-1.0.0.0.1',
                        '255.256.255.255']
        for dest in invalid_dest:
            self.assertRaises(socket.gaierror, wol.send_magic_packet,
                              self.sample_mac, dest=dest)

    def test_invalid_port(self):
        for p in [-1, -2, -3, 65536, 65537, 65538]:
            self.assertRaises(OverflowError, wol.send_magic_packet,
                              self.sample_mac, port=p)
        
