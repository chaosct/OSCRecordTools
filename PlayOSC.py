#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cPickle
import gzip
import time
import socket

def send(p):
    Socket.sendto(p, (host, port))

def main(filename,repeat):
    global Socket

    Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    first = True
    while first or repeat:
        first = False
        inFile = gzip.open(filename,'r')
        unpickler = cPickle.Unpickler(inFile)
        try:
            t,p = unpickler.load()
            baseline = t
            inittime = time.time()
            while 1:
                ts = t - baseline;
                mts = time.time() - inittime
                if (ts > mts):
                    time.sleep(ts - mts)
                send(p)   
                t,p = unpickler.load()
        except EOFError:
            pass
        except KeyboardInterrupt:
            repeat = False
        
if __name__ == '__main__':
    from optparse import OptionParser
    usage = "usage: %prog [options] inputFile"
    parser = OptionParser(usage=usage)
    parser.add_option("-r", "--repeat",
                  action="store_true", dest="repeat",
                  help="Autorepeat forever", default=False)
    parser.add_option("-t","--host", type="string", dest="host", default="localhost", help="Destination host(localhost)")
    parser.add_option("-p","--port", type="int", dest="port", default=3333, help="Destination port(3333)")
    
    (options, args) = parser.parse_args()
    port = options.port
    host = options.host
    if len(args) != 1:
        parser.error("incorrect number of arguments")

    main(args[0],options.repeat)
