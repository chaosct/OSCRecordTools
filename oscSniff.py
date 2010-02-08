import pcapy
from pcapy import open_live
from threading import Thread
import impacket
from impacket.ImpactDecoder import EthDecoder, LinuxSLLDecoder
import OSC

addressManager = 0 
oscThread = 0

class OSCServer(Thread) :
    def __init__(self, dev='any', port = 3333, ignoreIp = None) :
        Thread.__init__(self)
        DEV          = dev  # interface to listen on
	MAX_LEN      = 1514    # max size of packet to capture
	PROMISCUOUS  = 1       # promiscuous mode?
	READ_TIMEOUT = 100     # in milliseconds
	self.MAX_PKTS     = -1      # number of packets to capture; -1 => no limit
	self.p = open_live(DEV, MAX_LEN, PROMISCUOUS, READ_TIMEOUT)
	myfilter = 'udp and port '+str(port)
	if ignoreIp:
		myfilter+=' and not dst host '+ignoreIp
	self.p.setfilter(myfilter)
	self.callback = addressManager.handle
	self.packets = 0
	datalink = self.p.datalink()
        if pcapy.DLT_EN10MB == datalink:
            self.decoder = EthDecoder()
        elif pcapy.DLT_LINUX_SLL == datalink:
            self.decoder = LinuxSLLDecoder()
        else:
            raise Exception("Datalink type not supported: " % datalink)
            
    def ph(self,hdr, data):
	p = self.decoder.decode(data)
        ip = p.child()
        udp = ip.child()
        self.packets+=1
        self.callback( udp.get_data_as_string())
            
    def run(self) :
    	self.p.loop(self.MAX_PKTS,self.ph)

def init() :
    """ instantiates address manager and outsocket as globals
    """
    global addressManager
    addressManager = OSC.CallbackManager()


def listen(dev='any', port = 3333) :
    """  creates a new thread listening to that port 
    defaults to ipAddr='127.0.0.1', port 9001
    """
    global oscThread
    oscThread = OSCServer( dev, port )
    oscThread.start()

def bind(func, oscaddress):
    """ bind given oscaddresses with given functions in address manager
    """
    addressManager.add(func, oscaddress) 
    
def dontListen() :
    pass
    
if __name__ == '__main__':
    # example of how to use oscAPI
    init()
    listen() # defaults to "127.0.0.1", 9001

    # add addresses to callback manager
    def printStuff(msg):
        """deals with "print" tagged OSC addresses
        """
        print "printing in the printStuff function ", msg
        print "the oscaddress is ", msg[0]
        print "the value is ", msg[2]

    #bind(printStuff, "/test")

    

    #dontListen()  # finally close the connection bfore exiting or program

