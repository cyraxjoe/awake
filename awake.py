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
from __future__ import with_statement
import sys
import re
from optparse import OptionParser

import wol

def file_parser(fname, sep='\n'):
    """Parses the content of a file <fname>, returning the
    content separated with <sep>"""
    
    if int(sys.version[2]) < 5:
        chunks = []
        file_ = open(fname)
        for chunk in file_.read().split(sep):
            if chunk:
                chunks.append(chunk.strip())
        file_.close()
    else:
        with open(fname) as file_:
            chunks = [c.strip() for c in file_.read().split(sep) if c]
            
    if not chunks:
        raise Exception('No macs coud be found in file %s' % fname)
    else:
        return chunks
            

def main():
    usage = 'usage: %prog [options] MAC1 [MAC2 MAC3 MAC...]'
    parser = OptionParser(usage=usage)
    parser.add_option('-p', '--port', dest='port', default=9, type='int',
                      help='Destination port. (Default 9)')

    bhelp = 'Broadcast ip of the network. (Default 255.255.255.255)'
    parser.add_option('-b', '--broadcast', dest='broadcast',
                      default='255.255.255.255', type='string',
                      help=bhelp)

    fhelp = 'Use a file with the list of macs, separated with -s, by default \n.'
    parser.add_option('-f', '--file', dest='file', type='string', 
                      help=fhelp)

    shelp = 'Pattern to be use as a separator with the -f option.'
    parser.add_option('-s', '--separator', dest='separator', type='string',
                      default='\n', help=shelp)
    
    parser.add_option('-q', '--quiet', action='store_true',
                      help='Do not output informative messages.',
                      default=False)

    options, args = parser.parse_args()

    if not options.file and len(args) < 1:
        _errmsg = 'Requires at least one MAC address or a list of MAC (-f).'
        parser.error(_errmsg)
    regx = r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}'\
           r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'
    iprex = re.compile(regx)

    if not iprex.match(options.broadcast):
        parser.error('Invalid broadcast ip')

    macrex = re.compile(r'^([0-9a-fA-F]{2}([:-]|$)){6}$')
    l = len(args)

    if l > 0:
        macs = args
    else:
        macs = []
        
    if options.file:
        try:
            macs += file_parser(options.file, options.separator)
        except Exception, e:
            print >> sys.stderr, e
        
    for mac in macs:
        if macrex.match(mac):
            wol.wol(mac, options.broadcast, options.port)
            if not options.quiet:
                print 'Sending magick packet to %s with MAC  %s and port %d' % \
                      (options.broadcast, mac, options.port )
        else:
            if l == 1:
                parser.error('Invalid mac %s'%mac)
            else:
                print >> sys.stderr, 'Invalid mac %s'%mac


if __name__ == '__main__':
    main()
    

