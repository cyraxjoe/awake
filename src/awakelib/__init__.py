#!/usr/bin/env python
#Awake: Short program (library) to "wake on lan" a remote host.
#    Copyright (C) 2011  Joel Juvenal Rivera Rivera  rivera@joel.mx
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
"""Utility funtions that helps to wake-on-lan a host."""

__version_info__ = ('0','7','1')
__version__ = '.'.join(__version_info__)

import socket
import struct


def wol(mac, broadcast='255.255.255.255', dest=None, port=9):
    """Send  a "magic packet" to the given destination mac to wakeup 
    the host, if `dest` is not specified then the packed is broadcasted.
    """
    magicpkt = ''.join([struct.pack('6B', *[0xff] * 6),
                         struct.pack('96B', *[int(d, 16)
                                              for d in mac.split(':')] * 16)])
    sok = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sok.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    if dest is None:
        sok.connect((broadcast, port))
    else:
        sok.connect((dest, port))
    sok.send(magicpkt)
    sok.close()
