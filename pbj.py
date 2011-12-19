''' PBJ
    Camden Clements
    Adam Hodges
    Zach Welch
    
    pbj.py
'''

# activate virtualenv
import os
activate_this = os.path.expanduser("env/bin/activate_this.py")
execfile(activate_this, dict(__file__=activate_this))

import pickle
import time
import threading

import httpcli as http

GATEWAY_ADDR = '10.125.3.145'
TIME_TO_LIVE = 7

class searchReq:
    '''request for a keyword to be passed between nodes'''
    def __init__(self, searchid, filename, port=None):
        '''constructor'''
        self.ttl = TIME_TO_LIVE
        self.filename = filename
        self.searchid=searchid
        self.requestor=None
        self.requestorport=port
        self.timeinit = time.time()
        self.lastUltranode = None
        self.hops = 0

class Client:
    '''actual client code for node'''
    def __init__(self, path='share', port=5000):
        '''constructor'''
        self.isUltra = None     # boolean
        self.upId = None
        self.peers = []   # list of connected peers
        self.upeers = []  # list of connected ultrapeers
        self.upeer = None # ultrapeer of node
        self.searchctr = 0
        self.completedSearches = {}
        self.share = path
        self.port = port

    def getUpeers(self):
        '''return connected ultra peers'''
        if(self.isUltra):
            upeers=self.upeers
        else:
            upeers=self.upeer
        return upeers

    def connectToNetwork(self):
        '''Establish connection with gateway and process result'''
        data = http.send_register(self.port, GATEWAY_ADDR)
        data = pickle.loads(data)

        if data['isUltra']:
            # node is an ultrapeer
            self.isUltra = True
            self.upId = data['upId']
            self.upeers = data['uPeers']
            # connect to listed ultrapeers
            if self.upeers is not None:
                for up in self.upeers:
                    http.send_imaupeer(self.port, up)
        else:
            # node is not ultrapeer
            self.isUltra = False
            self.upeer = data['uPeer']
            # connect to listed ultrapeer
            if http.send_imapeer(self.port, self.upeer) is False:
                time.sleep(5)
                self.reconnect()
        t=threading.Thread(target=self.pingNodes)
        t.start()    

    def reconnect(self):
        '''reconnect to gateway after lost ultrapeer'''
        self.isUltra = None     # boolean
        self.peers = []   # list of connected peers
        self.upeers = []  # list of connected ultrapeers
        self.upeer = None # ultrapeer of node
        self.searchctr = 0
        self.completedSearches = {}
        data = http.send_register(self.port, GATEWAY_ADDR)
        data = pickle.loads(data)

        if data['isUltra']:
            self.isUltra = True
            self.upId=data['upId']
            if data['uPeers'] is not None:
                self.upeers = data['uPeers']
            if self.upeers is not None:
                for up in self.upeers:
                    http.send_imaupeer(self.port, up)

        else:
            self.isUltra = False
            self.upeer = data['uPeer']
            if http.send_imapeer(self.port, self.upeer) is False:
                time.sleep(5)
                self.reconnect()


    def pingNodes(self):
        '''ping all connected ultra peers and sub peers, removing them if no reply.
            if self is not an ultrapeer, reconnect to gateway if lost ultrapeer
        '''
        while True:

            time.sleep(5)
            if(self.isUltra):
                if self.upeers is not None:
                    for up in self.upeers:
                        if(http.send_ping(up) is False):
                            self.upeers.remove(up)
                if self.peers is not None:
                    for p in self.peers:
                        if(http.send_ping(p) is False):
                            self.peers.remove(p)
                            http.send_gateway_remove_peer(p)
                            #update gateway peer count
            else:
                if(http.send_ping(self.upeer) is False):
                    time.sleep(5)
                    self.reconnect()

    def checkForFile(self,filename):
        '''search for a file in the share directory'''
        foundFiles = []
        for root, dirs, files in os.walk(self.share):
            for name in files:
                if name != "results.csv":
                    if name.lower().find(filename.lower()) != -1:
                        newFile = root + '/' + name
                        prev,split,post = newFile.partition(self.share+'/')
                        foundFiles.append(post)
        return foundFiles
    
    def handleSearch(self, req):
        '''gets called by flask, universal (recursive) search function'''
        #requestor is null when requestor=self
        if(self.isUltra):
            req.lastUltranode=self.upId

        requestorname=""
        if req.requestor is not None:
            req.ttl = req.ttl-1
            req.hops = req.hops+1

            requestorname=req.requestor+":"+req.requestorport

            if(requestorname not in self.completedSearches):
                self.completedSearches[requestorname]=[]

            if (req.searchid in self.completedSearches[requestorname]): #or req.ttl<=0:
                return

            self.completedSearches[requestorname].append(req.searchid)
                
            for foundFile in self.checkForFile(req.filename):
                #found file
                req.path = foundFile
                http.send_found(self.port, req)
                #return
        
        if(self.isUltra):
            if self.peers is not None:
                for p in self.peers:
                    if p != requestorname:
                        http.send_search(req, p)
            
            if self.upeers is not None:    
                for up in self.upeers:
                    if up != requestorname:
                        #http.send req to connected upeer
                        http.send_search(req, up)
        else:
            if self.upeer != requestorname:
                http.send_search(req, self.upeer)

    def addPeer(self, p):
        '''add a peer to an ultra node'''
        if self.peers is None:
            self.peers=[p]
        else:
            self.peers.append(p)
    
    def addUPeer(self, up):
        '''connect this ultra peer with another'''
        if self.upeers is None:
            self.upeers=[up]
        else:
            self.upeers.append(up)

    def search(self, filename):
        '''create search request for filename'''
        req=searchReq(self.searchctr, filename, self.port)
        self.searchctr=self.searchctr+1
        self.handleSearch(req)

    def download(self, path):
        '''download file specified by arg path to share directory'''
        http.download(os.path.basename(path), path, self.share)
