Awake
==================================================================
*Short program (library) to "wake on lan" a remote host.*

If you  want to know something more about the WoL stuff check 
`the wikipedia page`_.
::
   
    Usage: awake.py [options] MAC1 [MAC2 MAC3 MAC...]
    
        Options:
          --version             show program's version number and exit
          -h, --help            show this help message and exit
          -p PORT, --port=PORT  Destination port. (Default 9)
          -b BROADCAST, --broadcast=BROADCAST
                                Broadcast ip of the network. (Default 255.255.255.255)
          -a ADDRESS, --address=ADDRESS
                                Address to connect and send the packet, by default use
                                the broadcast.
          -f FILE, --file=FILE  Use a file with the list of macs, separated with -s,
                                by default \n.
          -s SEPARATOR, --separator=SEPARATOR
                                Pattern to be use as a separator with the -f option.
          -q, --quiet           Do not output informative messages.

CLI Examples
------------

*Wake-on-lan a group of computers in the current network*::

    awake.py MAC1 MAC2 MAC3 MAC4 MACn

which is equivalent to::

    awake.py -f ~/list_of_macs

and in the file `list_of_macs` have one MAC per line or use the `-s` option.

*Wake-on-lan a computer or group of computers in a extenal network*

For this situation, you need to forward a port in your router, for example to
forward 9999 to 9 in the localnetwork o 7777 to 7, check the documentation if 
your router or modem. After the port has been configured you can use `DDNS`_
to have a reference to the current ip address of your router/modem and use awake
in this way::

    awake.py -a myhouse.homedns.com -p 9999 -f ~/file_with_my_macs 
   
or use any other option, the importan here is to use the `-a` and `-p` options 
to specify the destination to send the magic packet.


As a library
------------

The real functionality of the wake-on-lan is provided from a short function 
that is implemented in the provided module `wol`::

    wol(mac, broadcast='255.255.255.255', dest=None, port=9)
        Send  a "magic packet" to the given destination mac to wakeup 
        the host, if `dest` is not specified then the packed is broadcasted.


Apart from the awake script the WOL functionality can be easily integrated
in your python programs with a simple call to the function like::

    import wol
    def sysadmin_function_x(mac, *args):
        # some stuff...
        wol.wol(mac)
        # some more stuff...
    

Improvements, bugs?
-------------------

For any improvement or bug, feel free to create an `issue`_ in the github project.

.. _the wikipedia page: http://en.wikipedia.org/wiki/Wake-on-LAN
.. _DDNS: http://en.wikipedia.org/wiki/DDNS
.. _issue: http://github.com/cyraxjoe/awake/issues
