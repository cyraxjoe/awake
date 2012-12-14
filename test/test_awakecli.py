# -*- coding: utf-8 -*-
import os
import sys
import difflib
import unittest
import subprocess
import tempfile
from subprocess import CalledProcessError

from awake.utils import fetch_last_exception

import _test_utils
# Always decode the output of the errors for  py3 compatibility.

class TestCli(unittest.TestCase):

    def setUp(self):
        self.sample_mac = '1c:6f:66:31:e2:5f'
        self.awake_path = \
               os.path.join(os.path.dirname(sys.executable),
                            'awake')


    def __test_file_with_lines(self, lines, *macs_to_seek):
        path = self._create_sample_file(*lines)
        try:
            output = self._safe_execute('-f', path)
            for mac in macs_to_seek:
                self.assertIn('MAC %s' % mac, output)
        finally:
            os.remove(path)

            
    def _expect_error_and_assert_output(self, expoutput, *cmdargs):
        """Execute the subprocess command expecting an error and then
        validate that the `expoutput` is in the output of the command.
        """
        try:
            self._execute(*cmdargs)
        except CalledProcessError:
            exep = fetch_last_exception()
            output = exep.output.decode()
            if isinstance(expoutput, list) or  isinstance(expoutput, tuple):
                for emsg in expoutput:
                    self.assertIn(emsg, output)
            else:
                self.assertIn(expoutput, output)
        else:
            raise Exception('The process does not rise the '\
                            'expected exception CalledProcessError.')
            

    def _create_sample_file(self, *lines):
        """General abstraction to be used with the -f commands.
        Keep in mind that you need to delete the created file,
        just to be cleaner.
        """
        if not lines:
            lines = (self.sample_mac, )
        return _test_utils.create_sample_file(*lines)
            

    def _execute(self, *args):
        cmd = [self.awake_path, ] + list(args)
        return subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode()

        
    def _safe_execute(self, *args):
        """Execute the command and in case that a subprocess error show
        the outout of the executed command.
        """
        try:
            return self._execute(*args)
        except CalledProcessError:
            exp = fetch_last_exception()
            sys.stderr.write('\nDEBUG NOTE: %s\n' % exp.output)
            exp.message = exp.output
            raise exp

    
    def test_invalid_options(self):
        cmdargs = ['-x',]
        expected_output = 'awake: error: no such option: -x'
        self._expect_error_and_assert_output(expected_output, *cmdargs)


    def test_missing_required_argument(self):
        # Expection non-zero at the subprocess execution.
        expoutput = ('Requires at least one MAC'
                     ' address or a list of MAC (-f)')
        self._expect_error_and_assert_output(expoutput, )


    def test_1000_macs_in_args(self):
        macs = [self.sample_mac,] * 1000
        exp_messages = [('Sending magic packet to 255.255.255.255 with '\
                         'broadcast 255.255.255.255 MAC %s port 9' % \
                         self.sample_mac),] * 1000
        exp_output = '%s\n' % '\n'.join(exp_messages)
        output = self._execute(*macs)
        self.assertEqual(output, exp_output)


    def test_bad_mac_in_the_middle_of_args(self):
        macs = ['1c:6f:66:31:e2:5f',
                '1c:6f:66:31:e2:53',
                '1c:6f:66:31:e2:5X', # badmac
                '1c:6f:66:31:e2:11']
        expoutput = "Invalid MAC 1c:6f:66:31:e2:5X"
        self._expect_error_and_assert_output(expoutput, *macs)


    def test_quiet_option(self):
        cmdargs = ['-q', self.sample_mac]
        output = self._execute(*cmdargs).strip()
        self.assertEqual(output, '')


    def test_help_option(self):
        exp_output = \
        r"""Usage: awake [options] MAC1 [MAC2 MAC3 MAC...]

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -p PORT, --port=PORT  Destination port. (Default 9)
  -b BROADCAST, --broadcast=BROADCAST
                        Broadcast ip of the network. (Default 255.255.255.255)
  -d DESTINATION, --destination=DESTINATION
                        Destination ip/domain to connect and send the packet,
                        by default use broadcast.
  -f FILE, --file=FILE  Use a file with the list of macs, separated with -s,
                        by default \n. If any mac (line where -s \n), have the
                        "#" character, any following character is considered a
                        comment. Can be used multiple times for multiple
                        files.
  -s SEPARATOR, --separator=SEPARATOR
                        Pattern to be use as a separator with the -f option.
                        (Default \n)
  -q, --quiet           Do not output informative messages.
"""
        output = self._execute('--help')
        try:
            self.assertEqual(output, exp_output)
        except AssertionError:
            sys.stderr.write('\n\n\n')
            sys.stderr.write(''.join((difflib.unified_diff(output, exp_output, 
                                                           fromfile='a', tofile='b'))))
            sys.stderr.write('\n\n\n')
            raise 


    def test_dest_option(self):
        output = self._execute('-d', '127.0.0.1', self.sample_mac)
        self.assertIn('to 127.0.0.1', output)


    def test_port_option(self):
        output = self._execute('-p', '9999', self.sample_mac)
        self.assertIn('port 9999', output)


    def test_file_option(self):
        path = self._create_sample_file()
        try:
            output = self._safe_execute('-f', path)
            expected = 'MAC %s' % self.sample_mac
            self.assertIn(expected, output)
        finally:
            os.remove(path)

            
    def test_file_option_and_args(self):
        path = self._create_sample_file()
        othermac = '%s:ff' % self.sample_mac[:-3]
        try:
            output = self._safe_execute('-f', path, othermac)
            for expmsg in ['MAC %s' % m
                        for m in (self.sample_mac, othermac)]:
                self.assertIn(expmsg, output)
        finally:
            os.remove(path)


    def test_separation_option(self):
        mac_one = '111111111111'
        mac_two = '222222222222'
        macs = [self.sample_mac, mac_one, mac_two]
        line = '|'.join(macs)
        path = self._create_sample_file(line )
        try:
            output = self._safe_execute('-s', '|', '-f', path)
            for expmsg in ['MAC %s' % m for m in macs]:
                self.assertIn(expmsg, output)
        finally:
            os.remove(path)
            

    def test_multiple_file_options(self):
        mac_one = self.sample_mac
        mac_two = '111111111111'
        sone_path = self._create_sample_file()
        stwo_path = self._create_sample_file(mac_two)
        try:
            output = self._safe_execute('-f', sone_path, '-f', stwo_path)
            for expmsg in ['MAC %s' % m
                           for m in (mac_one, mac_two)]:
                self.assertIn(expmsg, output)
        finally:
            try:
                os.remove(sone_path)
            finally:
                os.remove(stwo_path)
        

    def test_file_with_in_line_comments(self):
        lines = ['%s  # this is a sample comment' % self.sample_mac, ]
        self.__test_file_with_lines(lines, self.sample_mac)


    def test_file_with_comment_per_line(self):
        lines = ['# this is full line of comment',
                 self.sample_mac]
        self.__test_file_with_lines(lines, self.sample_mac)

        
    def test_file_with_mixed_comments(self):
        othermac = '222222222222'
        lines = ['# this is full line of comment',
                 self.sample_mac,
                 '%s # comment' % othermac]
        self.__test_file_with_lines(lines, self.sample_mac, othermac)


    def test_not_exists_file(self):
        path = tempfile.mktemp('.awaketest')
        args = ['-f', path]
        self._expect_error_and_assert_output('Unable to parse the file', *args)
        

    def test_unable_to_read_file(self):
        path = self._create_sample_file()
        try:
            os.chmod(path, 0000)
            args = ['-f', path]
            self._expect_error_and_assert_output('Unable to parse the file',
                                                 *args)
        finally:
            os.remove(path)

    
    def test_bad_macs_in_file(self):
        good_macs = [self.sample_mac,
                     '111111111111']
        bad_macs = ['12asfasbbbnasnd',
                    '1212#413##424']
        macs = good_macs + bad_macs
        path = self._create_sample_file(*macs)
        try:
            args = ['-f', path]
             # the split is to eliminate the comment
            messages = ['Invalid MAC %s' % m.split('#', 1)[0]
                        for m in bad_macs]
            self._expect_error_and_assert_output(messages, *args)
        finally:
            os.remove(path)
    
