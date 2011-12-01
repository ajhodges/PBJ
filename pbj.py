# activate virtualenv
import os
activate_this = os.path.expanduser("env/bin/activate_this.py")
execfile(activate_this, dict(__file__=activate_this))

#import socket
import pickle

from httpcli import send_register, send_search, send_imapeer, send_imaupeer, send_found

GATEWAY_ADDR = 'gecko6.cs.clemson.edu'
TIME_TO_LIVE = 7

class searchReq:
    def __init__(self, searchid, filename, requestor=None):
        self.ttl = TIME_TO_LIVE
        self.filename = filename
        self.searchid=searchid
        self.requestor=requestor

class Client:
    def __init__(self, path='share'):
        self.isUltra = None     # boolean
        self.peers = []   # list of connected peers
        self.upeers = []  # list of connected ultrapeers
        self.upeer = None # ultrapeer of node
        self.searchctr = 0
        self.completedSearches = {}
        self.share = path

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
        data = send_register(GATEWAY_ADDR)
        data = pickle.loads(data)

        if data['isUltra']:
            self.isUltra = True
            self.upeers = data['uPeers']
            if self.upeers is not None:
                for up in self.upeers:
                    send_imaupeer(up)
        else:
            self.isUltra = False
            self.upeer = data['uPeer']
            send_imapeer(self.upeer)

    def checkForFile(self,filename):
        foundFiles = []
        for root, dirs, files in os.walk(self.share):
            for name in files:
                if name.lower().find(x.lower()) != -1:
                    foundFiles.append(root + '/' + name)
        return foundFiles
    
    def handleSearch(self, req):
        #requestor is null when requestor=self
        if req.requestor is not None:
            req.ttl = req.ttl-1

            if(req.requestor not in self.completedSearches):
                self.completedSearches[req.requestor]=[]

            if (req.searchid in self.completedSearches[req.requestor]) or req.ttl<=0:
                return

            self.completedSearches[req.requestor].append(req.searchid)
                
            for foundFile in self.checkForFile(req.filename):
                #found file
                send_found(req.requestor, foundFile)
                return
            
        if(self.isUltra):
            if self.peers is not None:
                for p in self.peers:
                    if p is not req.requestor:
                        send_search(req, p)
            
            if self.upeers is not None:    
                for up in self.upeers:
                    #send req to connected upeer
                    if up is not req.requestor:
                        send_search(req, up)
        else:
            if self.upeer is not req.requestor:
                send_search(req, self.upeer)

    def addPeer(self, p):
        if self.peers is None:
            self.peers=[p]
        else:
            self.peers.append(p)
    
    def addUPeer(self, up):
        if self.upeers is None:
            self.upeers=[up]
        else:
            self.upeers.append(up)

    def search(self, filename):
        req=searchReq(self.searchctr, filename)
        self.searchctr=self.searchctr+1
        self.handleSearch(req)
