# -*- coding: utf-8 -*-
import os
import unittest
import string

from awakelib import utils
from awakelib import wol

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
    pass


class TestWOL(unittest.TestCase):

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
        invalid_broadcasts = ['0.1.1.1.1',
                              '0.2.3.4.5',
                              '255.255.255.256',
                              '1.5.2.300']
        for bc in invalid_broadcasts:
            try:
                wol.send_magic_packet('11:11:11:11:11:11', bc)
            except ValueError:
                e = utils.fetch_last_exception()
                self.assertIn('Invalid broadcast', e.args[0])
            else:
                emsg = "The broadcast '%s' should not pass the test! " % bc
                raise AssertionError(emsg)
            

    def test_invalid_dest(self):
        raise NotImplementedError()

    def test_invalid_port(self):
        raise NotImplementedError()
    
    
