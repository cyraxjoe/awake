import sys
import re

_broregx = r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}'\
          r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'

brorex = re.compile(_broregx)

def _split_file(fname, sep='\n'):
    """Parses the content of a file <fname>, returning the
    content separated with `sep`.
    Basically `return file.read().split(sep)`"""
    chunks = []
    
    file_ = open(fname)
    for chunk in file_.read().split(sep):
        if chunk:
            chunks.append(chunk.strip())
    file_.close()
    
    return chunks


def _is_hexnumber(number):
    try:
        return bool(int(number, 16))
    except ValueError:
        return False

    
def _strip_separator_from_mac(mac):    
    if len(mac) == 12:
        return mac
    elif len(mac) == 12 + 5:
        separator = mac[2]
        return mac.replace(separator, '')
    else:
        raise ValueError('Invalid MAC %s' % mac)


def fetch_last_exception():
    """Utility function for compatibility purposes
    with python3 and 2"""
    return sys.exc_info()[1]


def is_valid_broadcast_ip(broadcast, rex=brorex):
    return rex.match(broadcast)


def retrive_MAC_digits(mac):
    plain_mac = _strip_separator_from_mac(mac)
    if _is_hexnumber(plain_mac):
        hexpairs = zip(plain_mac[::2],
                       plain_mac[1::2])
        return [''.join(digit) for digit in hexpairs]
    else:
        raise ValueError('Invalid MAC %s' % mac)
    
        
def fetch_macs_from_file(file_with_macs, sep):
    macs = []
    try:
        macs += _split_file(file_with_macs, sep)
    except Exception:
        exc = fetch_last_exception()
        errmsg = 'Unable to parse the file %s: %s' % (file_with_macs, exc)
        raise Exception(errmsg)
            
    return macs
            
