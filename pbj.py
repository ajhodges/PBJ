import socket
import pickle

GATEWAY_ADDR = 'gecko2.cs.clemson.edu'
TIME_TO_LIVE = 7

class searchReq:
    def __init__(self,filename):
        self.ttl = TIME_TO_LIVE
        self.filename = filename
        self.visited = []
    def addVisit(self,newVisList):
        self.visited = self.visited + newVisList

class Client:
    def __init__(self):
        self.isUltra = None     # boolean
        self.peers = []   # list of connected peers
        self.upeers = []  # list of connected ultrapeers
        self.upeer = None # ultrapeer of node

    def __str__(self):
        if(self.isUltra):
            string = "client info:\n  Rank: Ultrapeer\n  Connected ultrapeers: %s\n  Connected peers: %s\n" % (self.upeers, self.peers)
        else:
            string = "Client info:\n  Rank: Peer\n  Connected ultrapeer: %s\n" % self.upeer  
        return string

    def connectToNetwork(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.connect((GATEWAY_ADDR, 5555))
        data = sock.recv(102400)
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
    def search(self,filename):
        if checkForFile(filename) == True:
            #foundfile
            return
        for p in self.peers:
            if p.checkForFile(filename) == True:
                return
        req = searchReq(filename)
        req.addVisit(self.upeers)
        for up in self.upeers:
            pass
            #send req to upeer
    def handleSearch(self,req):
        req.ttl = req.ttl -1
        if(req.ttl > 0):
            for up in self.upeers:
                if up not in req.visited:
                    req.addVisit([up])
                    #send to up

def main():
    client = Client()
    client.connectToNetwork()
    print client

if __name__ == '__main__':
    main()
