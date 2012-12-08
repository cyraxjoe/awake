# -*- coding: utf-8 -*-
import os
import sys
import difflib
import unittest
import subprocess

from subprocess import CalledProcessError



from awakelib.utils import fetch_last_exception

# Always decode the output of the errors for
# py3 compatibility.

class TestCli(unittest.TestCase):

    def setUp(self):
        self.awake_path = \
                 os.path.join(os.path.dirname(sys.executable),
                              'awake')
        

    def _execute(self, *args):
        cmd = [self.awake_path, ] + list(args)
        return subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode()
    
    
    def test_invalid_options(self):
        cmdargs = ['-x']
        expected_output = 'awake: error: no such option: -x'
        
        try:
           self.assertEqual(self._execute(*cmdargs), None)
        except CalledProcessError:
            exep = fetch_last_exception()
            output = exep.output.decode() # for py3 compat.
            self.assertEqual(output.split('\n')[-2],
                             expected_output)
            

    def test_missing_required_argument(self):
        raise NotImplementedError()

    def test_1000_macs_in_args(self):
        sample_mac = '1c:6f:66:31:e2:5f'
    
        macs = [sample_mac,] * 1000

        exp_messages = [('Sending magic packet to 255.255.255.255 with MAC'
                         '  %s and port 9' % sample_mac),] * 1000
        exp_output = '%s\n' % '\n'.join(exp_messages)

        output = self._execute(*macs)
        self.assertEqual(output, exp_output)


    def test_bad_mac_in_the_middle_of_args(self):
        macs = ['1c:6f:66:31:e2:5f',
                '1c:6f:66:31:e2:53',
                '1c:6f:66:31:e2:5X', # badmac
                '1c:6f:66:31:e2:11']
        self.assertRaises(subprocess.CalledProcessError, self._execute, *macs)

    def test_quiet_option(self):
        sample_mac = '1c:6f:66:31:e2:5f'
        cmdargs = ['-q', sample_mac]
        
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
                        comment.
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
        raise NotImplementedError()

    def test_port_option(self):
        raise NotImplementedError()

    def test_file_option(self):
        raise NotImplementedError()

    def test_file_option_and_args(self):
        raise NotImplementedError()

    def test_separation_option(self):
        raise NotImplementedError()
    

    def test_multiple_file_options(self):
        raise NotImplementedError()




class TestFileOfMacsInCLI(unittest.TestCase):
    def test_big_file(self):
        raise NotImplementedError()


    def test_not_exists_file(self):
        raise NotImplementedError()


    def test_unable_to_read_file(self):
        raise NotImplementedError()

    
    def test_bad_macs_in_file(self):
        raise NotImplementedError()
    
        



    

        

        


