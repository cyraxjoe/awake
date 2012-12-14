import socket
import struct

from awake import utils


def send_magic_packet(mac, broadcast='255.255.255.255', dest=None, port=9):
    """Send  a "magic packet" to the given destination mac to wakeup
    the host, if `dest` is not specified then the packet is broadcasted.

    If the `mac` address can't be parsed raise `ValueError`.

    If `dest` is not a valid domain name or ip raise `socket.error`.
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
    try:
        if dest is None:
            sok.connect((broadcast, port))
        else:
            sok.connect((dest, port))
        sok.send(magicpkt)
    finally:
        sok.close()
