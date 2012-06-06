# -*- coding: utf-8 -*-
import os
import unittest
import string

from awakelib import utils

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
        raise NotImplementedError()

    def test_invalid_broadcast(self):
        raise NotImplementedError()

    def test_invalid_dest(self):
        raise NotImplementedError()

    def test_invalid_port(self):
        raise NotImplementedError()
    
    
