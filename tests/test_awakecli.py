# -*- coding: utf-8 -*-
import os
import sys
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
                              'awake.py')
        

    def _execute(self, *args):
        cmd = [self.awake_path, ]
        cmd += args
        return subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    
    
    def test_invalid_options(self):
        cmdargs = ['-x']
        expected_output = 'awake.py: error: no such option: -x'
        
        try:
           self.assertEqual(self._execute(*cmdargs), None)
        except CalledProcessError:
            exep = fetch_last_exception()
            output = exep.output.decode() # for py3 compat.
            self.assertEqual(output.split('\n')[-2],
                             expected_output)
            

    def test_missing_required_argument(self):
        pass

    def test_1000_macs_in_args(self):
        sample_mac = '1c:6f:66:31:e2:5f'
    
        macs = [sample_mac,] * 1000

        exp_messages = [('Sending magic packet to 255.255.255.255 with MAC'
                         '  %s and port 9' % sample_mac),] * 1000
        exp_output = '%s\n' % '\n'.join(exp_messages)

        output = self._execute(*macs).decode()
        self.assertEqual(output, exp_output)


    def test_bad_mac_in_the_middle_of_args(self):
        pass
    
    def test_quiet_option(self):
        pass

    def test_help_option(self):
        pass

    def test_dest_option(self):
        pass

    def test_port_option(self):
        pass

    def test_file_option(self):
        pass

    def test_file_option_and_args(self):
        pass

    def test_separation_option(self):
        pass
    

    def test_multiple_file_options(self):
        pass




class TestFileOfMacsInCLI(unittest.TestCase):
    def test_big_file(self):
        pass


    def test_not_exists_file(self):
        pass


    def test_unable_to_read_file(self):
        pass

    
    def test_bad_macs_in_file(self):
        pass
    
        



    

        

        


