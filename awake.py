#!/usr/bin/env python
#Short program (library) to "wake on lan"  a remote host.
#    Copyright (C) 2010  Joel Juvenal Rivera Rivera  joelriv@gmail.com
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

import socket
import struct

def wol(mac, broadcast='255.255.255.255', port=9):
    """ Send  "magick packet" to the given mac to wakeup the host."""
    magic_pkt = ''.join([struct.pack('6B', *[0xff] * 6),
                         struct.pack('96B',*[int(d, 16) for d in mac.split(':')] * 16)])
    sok = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sok.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sok.connect((broadcast, port))
    sok.send(magic_pkt)
    sok.close()
       
def _main():
    parser = OptionParser(usage='usage: %prog [options] MAC1 [MAC2 MAC3 MAC...]')
    parser.add_option('-p', '--port', dest='port', default=9, type='int',
                      help='Destination port, only 0, 7 or 9. (Default 9)')
    parser.add_option('-b', '--broadcast', dest="broadcast",
                      default='255.255.255.255', type='string',
                      help='Broadcast ip of the network. (Default 255.255.255.255)')

    options, args = parser.parse_args()

    if len(args) < 1:
        parser.error('Requires at least one MAC address.')

    if not re.match(r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b',
                    options.broadcast):
        parser.error('Invalid broadcast ip')
    if options.port not in [0, 7, 9]:
        parser.error('Invalid port, only supports 0, 7 or 9.')
        
    macrex = re.compile(r'^([0-9a-fA-F]{2}([:-]|$)){6}$')
    l = len(args)
    for mac in args:
        if macrex.match(mac):
            wol(mac, options.broadcast, options.port)
            print 'Sending magick packet to %s with MAC  %s and port %d'%(options.broadcast, mac, options.port )
        else:
            if l == 1:
                parser.error('Invalid mac %s'%mac)
            else:
                print >> sys.stderr, 'Invalid mac %s'%mac


if __name__ == '__main__':
    import sys
    import re
    from optparse import OptionParser
    _main()
    
    
                    



    
