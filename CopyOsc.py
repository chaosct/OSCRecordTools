#!/usr/bin/env python
# -*- coding: utf-8 -*-

import oscSniff
import socket
import sys
import time

restartline = '\x1b[2K\x1b[0G'

class Sender(object):
	def __init__(self,host,port):
		self.HOST = host
		self.PORT = port
		self.Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	def send(self,data):
		self.Socket.sendto(data, (self.HOST, self.PORT))
	def close(self):
		pass

def main(host,port=3333):
	sender = Sender(host,port)
	oscserver = oscSniff.OSCServer(sender.send,ignoreIp=host)
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
    
    if len(sys.argv) < 2:
	    print "usage: %s ip [port]" % sys.argv[0]
	    exit(0)
    host = sys.argv[1]
    port = 3333
    if len(sys.argv) > 2:
	    port = int(sys.argv[2])
    print 'Sending sniffed packets to %s:%d' % (host,port)
    main(host,port)
