#!/usr/bin/env python
# -*- coding: utf-8 -*-

import oscSniff
import sys
import time
import cPickle
import gzip

restartline = '\x1b[2K\x1b[0G'

class FileDumper(object):
	def __init__(self,path):
		self.outFile = gzip.open(path,'w')
		self.pickler = cPickle.Pickler(self.outFile)
	def send(self,data):
		tostore = (time.time(),data)
		self.pickler.dump(tostore)
	def close(self):
		self.outFile.close()
	

def main(port=3333):
    if len(sys.argv) < 2:
        print "usage: %s filename" % sys.argv[0]
        exit(0)
    filename = sys.argv[1]
    sender = FileDumper(filename)
    oscserver = oscSniff.OSCServer(sender.send)
    oscserver.start()
    try:
	    while 1:
		    time.sleep(1)
		    print restartline + "%d packets sniffed so far" % oscserver.packets ,
		    sys.stdout.flush()
    except KeyboardInterrupt:
	    sender.close()
	    exit(0)
	
	
if __name__ == '__main__':
	main()
