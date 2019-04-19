import socket
import struct

from awake import utils
from awake.errors import AwakeNetworkError


def _bind_socket(sok, bind_ip):
    # binding to 0 means, use any random port that
    # the OS has available
    random_port = 0
    try:
        sok.bind((bind_ip, random_port))
    except socket.error:
        exep = utils.fetch_last_exception()
        raise AwakeNetworkError(
            "Unable to bind to '%s'.\n"
            "\t Make sure the IP is correct and is assigned to one of your NICs.\n\n"
            "\t If you use a network address (first addres in the network), \n"
            "\t it will go into the default routing.\n\n"
            "Original error: %s" % (bind_ip, exep),
            original_error=exep
        )


def send_magic_packet(mac, broadcast='255.255.255.255', dest=None, port=9, bind_ip=None):
    """Send  a "magic packet" to the given destination mac to wakeup
    the host, if `dest` is not specified then the packet is broadcasted.

    If the `mac` address can't be parsed raise `ValueError`.

    If `dest` is not a valid domain name or ip raise `socket.error`.

    If `bind_ip ` is set, try to bind into that address/NIC before sending the packet.
    """
    try:
        if not utils.is_valid_broadcast_ip(broadcast):
            raise ValueError('Invalid broadcast %s' % broadcast)
    except TypeError:
        raise ValueError('Invalid broadcast %r' % broadcast)
    mac_digits = utils.retrive_MAC_digits(mac)
    magic_header = struct.pack('6B', *[0xff] * 6)
    magic_body = struct.pack('96B', *[int(d, 16) for d in mac_digits] * 16)
    magicpkt = magic_header + magic_body
    sok = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sok.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    if bind_ip is not None:
        _bind_socket(sok, bind_ip)
    try:
        if dest is None:
            sok.connect((broadcast, port))
        else:
            sok.connect((dest, port))
        sok.send(magicpkt)
    finally:
        sok.close()
