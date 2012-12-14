import sys
from optparse import OptionParser

import awake


def _build_cliparser():
    usage = 'usage: %prog [options] MAC1 [MAC2 MAC3 MAC...]'
    parser = OptionParser(usage=usage,
                          version='%%prog: %s' % awake.__version__)
    parser.add_option('-p', '--port', dest='port', default=9, type='int',
                      help='Destination port. (Default 9)')
    bhelp = 'Broadcast ip of the network. (Default 255.255.255.255)'
    parser.add_option('-b', '--broadcast', dest='broadcast',
                      default='255.255.255.255', type='string',
                      help=bhelp)
    dhelp = 'Destination ip/domain to connect and send the packet, ' \
            'by default use broadcast.'
    parser.add_option('-d', '--destination', dest='destination', default=None,
                      help=dhelp)
    fhelp = 'Use a file with the list of macs, ' \
            'separated with -s, by default \\n. ' \
            'If any mac (line where -s \\n), have the "#" character, ' \
            'any following character is considered a comment. ' \
            'Can be used multiple times for multiple files.'
    parser.add_option('-f', '--file', dest='file',  action='append',
                      default=[], help=fhelp)
    shelp = 'Pattern to be use as a separator with the -f option. (Default \\n)'
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
        raise Exception(errmsg)    
    macs += args
    try:
        for file_with_macs in options.file:
            macs += awake.utils.fetch_macs_from_file(file_with_macs,
                                                     options.separator)
    except Exception:
        exep = awake.utils.fetch_last_exception()
        sys.stderr.write('%s\n' % exep.args)
    return macs
        

def _notify_error_and_finish(message, cliparser):
    cliparser.print_help() 
    cliparser.error(message)


def _send_packets(macs, broadcast, destination, port, quiet_mode):
    """Send a magic packet to each mac in *macs*, this function tries
    to deliver even if some of the macs are faulty in anyway.

    Returns False in case of any error on any of the *macs*, otherwise True.
    """
    no_errors = True
    for mac in macs:
        try:
            awake.wol.send_magic_packet(mac, broadcast, destination, port)
        except ValueError:
            exep = awake.utils.fetch_last_exception()
            sys.stderr.write('ERROR: %s\n' % exep.args[0])
            no_errors = False
        else:
            if not quiet_mode:
                if destination is None:
                    destination = broadcast
                print('Sending magic packet to %s with broadcast %s MAC %s port %d' % \
                      (destination, broadcast, mac, port))
    return no_errors


def main():
    cliparser = _build_cliparser()
    options, args = cliparser.parse_args()
    try:
        macs = _get_macs(options, args)
    except Exception:
        exep = awake.utils.fetch_last_exception()
        _notify_error_and_finish(exep.args[0], cliparser)
    if macs:
        if not _send_packets(macs, options.broadcast,
                             options.destination,
                             options.port, options.quiet_mode):
            sys.exit(1)
    else:
        _notify_error_and_finish('Unable to acquire any mac address',
                                 cliparser)
