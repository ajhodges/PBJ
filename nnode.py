# program models peer/ultrapeer network
# not fully scaleable (see comments below)

import sys
import math
import networkx as nx
import pygraphviz as pgv 

PEERS_PER_UPEER = 3 # constant

upeercount = 0    # number of ultrapeers in network

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
    names = ['A1', 'A2', 'A3', '1', 'B1', 'B2', 'B3', '2', 'C1', 'C2','C3','3','D1','D2','D3','4','E1','E2','E3','5','F1']
    for i in range(len(names)):
        n.newNode(names[i])   
    
    G = pgv.AGraph()
    n.makeGraph(G)
    G.layout()
    G.draw('file.png')

    print n.root.upeers
    sys.exit(0)


