#!/usr/bin/env python
#Awake: Short program (library) to "wake on lan"  a remote host.
#    Copyright (C) 2012  Joel Juvenal Rivera Rivera rivera@joel.mx
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
import sys

from optparse import OptionParser

import awakelib

from awakelib import utils
from awakelib import wol



def _build_parser():
    usage = 'usage: %prog [options] MAC1 [MAC2 MAC3 MAC...]'
    parser = OptionParser(usage=usage, version='%%prog: %s' % awakelib.__version__)
    parser.add_option('-p', '--port', dest='port', default=9, type='int',
                      help='Destination port. (Default 9)')

    bhelp = 'Broadcast ip of the network. (Default 255.255.255.255)'
    parser.add_option('-b', '--broadcast', dest='broadcast',
                      default='255.255.255.255', type='string',
                      help=bhelp)

    ahelp='Address to connect and send the packet,' \
          ' by default use the broadcast.'
    parser.add_option('-d', '--destination', dest='destination', default=None,
                      help=ahelp)

    fhelp = 'Use a file with the list of macs,' \
            ' separated with -s, by default \\n.'
    parser.add_option('-f', '--file', dest='file', type='string', 
                      help=fhelp)

    shelp = 'Pattern to be use as a separator with the -f option.'
    parser.add_option('-s', '--separator', dest='separator', type='string',
                      default='\n', help=shelp)
    
    parser.add_option('-q', '--quiet', dest='quiet_mode', action='store_true',
                      help='Do not output informative messages.',
                      default=False)

    return parser


def _get_macs(options, args):
    macs = []
    if not options.file and len(args) < 1:
        errmsg = 'Requires at least one MAC address or a list of MAC (-f).'
        _notify_error_and_finish(errmsg)
        
    if len(args): 
        macs += args

    if options.file: 
        try:
            macs += utils.fetch_macs_from_file(options.file,
                                               options.separator)
        except Exception:
            exep = utils.fetch_last_exception()
            sys.stderr.write('%s\n' % exep.args)
            
    return macs
        

def _send_packets(macs, broadcast, destination, port, quiet_mode):
    for mac in macs:
        try:
            wol.send_magic_packet(mac, broadcast, destination, port)
        except ValueError:
            exep = utils.fetch_last_exception()
            sys.stderr.write('%s\n' % exep.args[0])
            
        else:
            if not quiet_mode:
                print('Sending magic packet to %s with MAC  %s and port %d' % \
                      (broadcast, mac, port))


def main(options, args):
    try:
        macs = _get_macs(options, args)
    except Exception:
        exep = utils.get_last_exception()
        _notify_error_and_finish(exep.args)

    if macs:
        _send_packets(macs, options.broadcast, options.destination,
                      options.port, options.quiet_mode)
    else:
        _notify_error_and_finish('Unable to acquire any mac address')


def _notify_error_and_finish(message):
    # parser is defined in the global scope at the bottom.
    parser.print_help() 
    parser.error(message)

    
if __name__ == '__main__':
    parser = _build_parser()
    options, args = parser.parse_args()
    main(options, args)
    

