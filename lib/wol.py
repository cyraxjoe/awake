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
                         struct.pack('96B', *[int(d, 16)
                                              for d in mac.split(':')] * 16)])
    sok = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sok.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sok.connect((broadcast, port))
    sok.send(magic_pkt)
    sok.close()
