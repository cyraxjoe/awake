import sys
import warnings
import re

_broregx = r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}'\
          r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'

brorex = re.compile(_broregx)
macrex = re.compile(r'^([0-9a-fA-F]{2}([:-]|$)){6}$')


def _split_file(fname, sep='\n'):
    """Parses the content of a file <fname>, returning the
    content separated with <sep>"""
    chunks = []
    
    file_ = open(fname)
    for chunk in file_.read().split(sep):
        if chunk:
            chunks.append(chunk.strip())
    file_.close()
    
    return chunks

def _fetch_last_exception():
    """Utility function for compatibility purposes with python3 and 2"""
    return sys.exc_info()[1]
    

def is_valid_broadcast_ip(broadcast, rex=brorex):
    return rex.match(broadcast)


def is_valid_mac(mac, rex=macrex):
    return rex.match(mac)


def fetch_macs_from_file(file_with_macs, sep):
    try:
        macs = _split_file(file_with_macs, sep)
    except Exception:
        exc = _fetch_last_exception()
        errmsg = 'Unable to parse the file %s: %s' % (file_with_macs, exc)
        warnings.warn(errmsg)
            
    return macs
            
