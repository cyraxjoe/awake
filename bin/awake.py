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
import warnings
from optparse import OptionParser

import awakelib
from awakelib import utils
from awakelib import wol


def _build_cli():
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
    parser.add_option('-a', '--address', dest='address', default=None,
                      help=ahelp)

    fhelp = 'Use a file with the list of macs,' \
            ' separated with -s, by default \\n.'
    parser.add_option('-f', '--file', dest='file', type='string', 
                      help=fhelp)

    shelp = 'Pattern to be use as a separator with the -f option.'
    parser.add_option('-s', '--separator', dest='separator', type='string',
                      default='\n', help=shelp)
    
    parser.add_option('-q', '--quiet', action='store_true',
                      help='Do not output informative messages.',
                      default=False)

    return parser
    


def main():
    parser = _build_cli()
    options, args = parser.parse_args()
    
    if not options.file and len(args) < 1:
        _errmsg = 'Requires at least one MAC address or a list of MAC (-f).'
        parser.print_help()
        parser.error(_errmsg)


    if len(args) > 0:
        macs = args
    else:
        macs = []
        
    if options.file:
        macs += utils.fetch_macs_from_file(options.file, options.separator)
        
    for mac in macs:
        wol.send_magic_packet(mac, options.broadcast,
                              options.address,
                              options.port)
        if not options.quiet:
            print('Sending magick packet to %s with MAC  %s and port %d' % \
                  (options.broadcast, mac, options.port ))
        else:
            if len(args) == 1:
                parser.error('Invalid mac %s' % mac)
            else:
                warnings.warn('Invalid mac %s' % mac, SyntaxWarning)


if __name__ == '__main__':
    main()
    

