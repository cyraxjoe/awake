import sys
import re

# Broadcast regex.
_broregx = r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}'\
          r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'
brorex = re.compile(_broregx)

def _split_file(fname, sep='\n'):
    """Parses the content of a file <fname>, returning the
    content separated with `sep`.
    Basically `return file.read().split(sep)`"""
    chunks = []
    file_ = open(fname)
    try:
        for chunk in file_.read().split(sep):
            schunk = chunk.strip()
            if schunk:
                chunks.append(schunk)
    finally:
        file_.close()    
    return chunks


def _is_hexnumber(number):
    """Evalute the string `number` in case that the type
    is not valid the method returns False otherwise True.
    """
    try:
        return bool(int(number, 16))
    except (ValueError, TypeError):
        return False

    
def _strip_separator_from_mac(mac):
    # if is python2, convert to unicode to have
    # the right length in a character context.
    if sys.version_info[0] == 2:
        mac = mac.decode('utf-8')
    if len(mac) == 12:  # is the full mac, without separators.
        return mac
    elif len(mac) == 12 + 5:  # it has a separator (5 separators)
        separator = mac[2]
        return mac.replace(separator, '')
    else:
        raise ValueError('Invalid MAC %s [len %s]' % (mac, len(mac)))


def fetch_last_exception():
    """Utility function for compatibility purposes
    with python3 and 2"""
    return sys.exc_info()[1]


def is_valid_broadcast_ip(broadcast, rex=brorex):
    return bool(not broadcast.startswith('0.') and \
                rex.match(broadcast))


def retrive_MAC_digits(mac):
    """Receives a string representing `mac` address
    with one or none separator for each two digits
    in the hex number.
       
    Valid:  aa:aa:aa:aa:aa:11
            aa-aa-AA-AA-aa-11
            FF@ff@AA@55@aa@11
            aaaaaaaaaa11
    Invalid:
            11:11:11:11-11-11
            11:11:11:111111
            11::11:11:11:11:11

   Return each two digits in a list.
   Raise ValueError in case that the `mac` does
   not fulfill the requirements to be valid.
   """
    try:
        plain_mac = _strip_separator_from_mac(mac)
    except (AttributeError, TypeError): # not a string
        raise ValueError('Invalid MAC %s (not a string)' % mac)
        
    if _is_hexnumber(plain_mac):
        hexpairs = zip(plain_mac[::2],
                       plain_mac[1::2])
        return [''.join(digit) for digit in hexpairs]
    else:
        raise ValueError('Invalid MAC %s' % mac)

        
def fetch_macs_from_file(file_with_macs, sep):
    """Read the macs from the specified path at *files_with_macs* using
    *sep* as a separator.
    
    If any mac (line for the most common case where *sep*=\n)
    have the "#" character, any following character is considered a
    comment until *sep*, this allows in-line comments or just a bunch of
    lines with comments.

    This function does not validate each mac just strip any comment and appened
    to a list.
    """
    macs = []
    try:
        for line in _split_file(file_with_macs, sep):
            if line.startswith('#'): # is a comment
                continue
            else:
                comtidx = line.find('#')  # look for in-line comments
                if comtidx > -1:
                    mac = line[:comtidx].strip()  # remove the comment
                else:
                    mac = line
            macs.append(mac)
    except Exception:
        exc = fetch_last_exception()
        errmsg = 'Unable to parse the file %s: %s' % (file_with_macs, exc)
        raise Exception(errmsg)
    return macs
