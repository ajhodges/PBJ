# activate virtualenv
''' PBJ
    Camden Clements
    Adam Hodges
    Zach Welch
    
    nnode.py simulates the network being built and creates a png visualization
    of the network. Used in designing system and algorithms
    '''


import os
activate_this = os.path.expanduser("env/bin/activate_this.py")
execfile(activate_this, dict(__file__=activate_this))

# program models peer/ultrapeer network
# not fully scaleable (see comments below)

import sys
import os
import math
import networkx as nx
import pygraphviz as pgv 

PEERS_PER_UPEER = 3 # constant
TIME_TO_LIVE = 7

upeercount = 0    # number of ultrapeers in network

class searchReq:
    def __init__(self,filename):
        self.ttl = TIME_TO_LIVE
        self.filename = filename
        self.visited = []
    def addVisit(self,newVisList):
        self.visited = self.visited + newVisList

class Node:
    def __init__(self, name, isUltra):
        global upeercount
        print "Creating new node: %s." % (name)
        self.name = name        # name of peer (address)
        self.isUltra = isUltra  # boolean
        self.peers = []         # list of connected peers
        self.upeers = {}        # dict of connected ultrapeers
        if(isUltra):
            upeercount = upeercount + 1
            self.upeerid = upeercount
            print "It is now ultrapeer %d." % upeercount

    def isUltraPeer(self):
        return self.isUltra
    def getUpeers(self):
        return self.upeers
    def getName(self):
        return self.name
    def getPeers(self):
        return self.peers
    def getUpeerid(self):
        return self.upeerid
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
        req.addVisit(self.upeers.get_keys())
        for up in self.upeers.get_keys():
            pass
            #send req to upeer
    def handleSearch(self,req):
        req.ttl = req.ttl -1
        if(req.ttl > 0):
            for up in self.upeers.get_keys():
                if up not in req.visited:
                    req.addVisit([up])
                    #send to up

class Network:
    def __init__(self):
        print "Creating Network."
        self.root = Node('0', True)

    def findUPeer(self, up):
        if(len(up.peers) < PEERS_PER_UPEER):
            return up
        elif up.upeers.keys() != []:
            if up.upeers[max(up.upeers.keys())].upeerid > up.upeerid:
                return self.findUPeer(up.upeers[max(up.upeers.keys())])

    # doesn't work for more than 4 ultrapeers
    def linkUPeer(self, up):
        curup = self.root
        
        while(curup.upeerid != up.upeerid):
            
            if(math.log((up.upeerid - curup.upeerid), 2) % 2 == 0):
                print "Linking ultrapeers %d and %d." % (curup.upeerid, up.upeerid)
                up.upeers[curup.upeerid - up.upeerid] = curup
                curup.upeers[up.upeerid - curup.upeerid] = up
                
            # some how need to traverse ultrapeers sequitially
            
            curup = curup.upeers[1]



    def newNode(self, name):
        upeer = self.findUPeer(self.root)
        if upeer is None:
            newnode = Node(name, True)
            self.linkUPeer(newnode)
        else:
            print "Found upeer ",str(upeer.upeerid)

            newnode = Node(name, False)
            upeer.peers.append(newnode)
            print "Node %s added to Ultrapeer %s" % (newnode.name, upeer.upeerid)
   
    
    def getRoot(self):
        return self.root
    
    
    def makeSubGraph(self,uPeer,Graph,Visited):
        for subPeer in uPeer.getPeers():
            Graph.add_node(subPeer.getName())
            Graph.add_edge(uPeer.getName(),subPeer.getName())
        hold = uPeer.getUpeers()
        if hold != {}:
            for key in hold.keys():
                if key > 0:
                    Graph.add_node(uPeer.upeers[key].getName())
                    Graph.add_edge(uPeer.getName(),uPeer.upeers[key].getName())
            if uPeer.upeers.has_key(1):
                self.makeSubGraph(uPeer.upeers[1],Graph,Visited)
            
#            print Visited
#           print up.getName()
                #           if up.getName() in Visited:
#          pass
                #            else:
                #         Graph.add_node(up.getName())
                #       Graph.add_edge(uPeer.getName(),up.getName())
                #       Visited.append(uPeer.getName())
#   self.makeSubGraph(up,Graph,Visited)

    def makeGraph(self,Graph):
        Graph.add_node(self.root.getName())
        visited = []
        self.makeSubGraph(self.root,Graph,visited)

    

if __name__ == '__main__':
    # create a network and add 10 additional nodes
    n = Network()
    names = ['0-1', '0-2', '0-3', '1','1-1', '1-2', '1-3','2','2-1', '2-2', '2-3','3','3-1', '3-2', '3-3','4','4-1', '4-2', '4-3']
    for i in range(len(names)):
        n.newNode(names[i])   
    
    G = pgv.AGraph()
    n.makeGraph(G)
    G.layout()
    G.draw('file.png')

    print n.root.upeers
    sys.exit(0)


