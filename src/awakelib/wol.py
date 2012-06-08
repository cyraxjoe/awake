#Awake: Short program (library) to "wake on lan"  a remote host.
#    Copyright (C) 2012  Joel Juvenal Rivera Rivera rivera@joel.mx
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License version 3
#    as published by the Free Software Foundation.
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

from awakelib import utils


def send_magic_packet(mac, broadcast='255.255.255.255', dest=None, port=9):
    """Send  a "magic packet" to the given destination mac to wakeup 
    the host, if `dest` is not specified then the packed is broadcasted.

    If the `mac` address is unable to be parsed
    `ValueError` get raised. (yes it rhymes).

    If `dest` is not a valid domain name or ip raise socket.error.
    """
    try:
        if not utils.is_valid_broadcast_ip(broadcast):
            raise ValueError('Invalid broadcast %s' % broadcast)
    except TypeError:
        raise ValueError('Invalid broadcast %r' % broadcast)
    
    mac_digits = utils.retrive_MAC_digits(mac)
    
    magic_header = struct.pack('6B', *[0xff] * 6)
    magic_body = struct.pack('96B', *[int(d, 16)
                                      for d in mac_digits] * 16)
    magicpkt = magic_header + magic_body
    
    sok = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sok.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    if dest is None:
        sok.connect((broadcast, port))
    else:
        sok.connect((dest, port))
    sok.send(magicpkt)
    sok.close()
