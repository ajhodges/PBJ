#import socket
import pickle

from httpcli import send_register, send_search

GATEWAY_ADDR = 'localhost'
TIME_TO_LIVE = 7

class searchReq:
    def __init__(self, searchid, filename, requestor=None):
        self.ttl = TIME_TO_LIVE
        self.filename = filename
        self.searchid=searchid
        self.requestor=requestor

class Client:
    def __init__(self):
        self.isUltra = None     # boolean
        self.peers = []   # list of connected peers
        self.upeers = []  # list of connected ultrapeers
        self.upeer = None # ultrapeer of node
        self.searchctr = 0
        self.completedSearches = []

    def __str__(self):
        if(self.isUltra):
            string = "client info:\n  Rank: Ultrapeer\n  Connected ultrapeers: %s\n  Connected peers: %s\n" % (self.upeers, self.peers)
        else:
            string = "Client info:\n  Rank: Peer\n  Connected ultrapeer: %s\n" % self.upeer  
        return string

    def getUpeers(self):
        if(self.isUltra):
            upeers=self.upeers
        else:
            upeers=self.upeer
        return upeers

    def connectToNetwork(self):
#        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#        sock.connect((GATEWAY_ADDR, 5555))
#        data = sock.recv(102400)
        data = send_register(GATEWAY_ADDR)
        data = pickle.loads(data)
        if data['isUltra']:
            self.isUltra = True
            self.upeers = data['uPeers']
            # tell upeers about this
        else:
            self.isUltra = False
            self.upeer = data['uPeer']
            # tell upeer about this

    def checkForFile(self,filename):
         return os.path.isfile('share/' + filename)   
    
    def handleSearch(self, req):
        #requestor is null when requestor=self
        if req.requestor is not None:
            req.ttl = req.ttl-1
            if (req.searchid in self.completedSearches) or req.ttl<=0:
                return
            self.completedSearches.add(req.searchid)
            
            if checkForFile(req.filename) == True:
                #found file
                send_found(req.requestor, req.filename)
                return
            
        if(self.isUltra):
            for p in self.peers:
                send_search(req, p)
                
            for up in self.upeers:
                #send req to connected upeer
                send_search(req, up)
        else:
            send_search(req, self.upeer)
            
    def search(self, filename):
        req=searchReq(self.searchctr, filename)
        self.searchctr=self.searchctr+1
        self.handleSearch(req)     
            

#def main():
#    client = Client()
#    client.connectToNetwork()
#    client.search("wat")
#    print client

if __name__ == '__main__':
    main()
