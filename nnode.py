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
        self.upeers = []        # list of connected ultrapeers
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
        self.root = Node('A', True)

    def findUPeer(self, up):
        if(len(up.peers) < PEERS_PER_UPEER):
            return up
        else:
            for peer in up.upeers:
                if(peer.upeerid > up.upeerid):
                    return self.findUPeer(peer)

    # doesn't work for more than 4 ultrapeers
    def linkUPeer(self, up):
        curup = self.root
        i = 0
        while(curup.upeerid != up.upeerid):
            if(math.log((up.upeerid - curup.upeerid), 2) % 2 == 0):
                print "Linking ultrapeers %d and %d." % (curup.upeerid, up.upeerid)
                up.upeers.append(curup)
                curup.upeers.append(up)
                i=0
            # some how need to traverse ultrapeers sequitially
            if(curup.upeers[i].upeerid > curup.upeerid):
                curup = curup.upeers[i]
                i = i+1
            else:
                break            

    def newNode(self, name):
        upeer = self.findUPeer(self.root)
        if upeer is None:
            newnode = Node(name, True)
            self.linkUPeer(newnode)
        else:
            newnode = Node(name, False)
            upeer.peers.append(newnode)
            print "Node %s added to Ultrapeer %s" % (newnode.name, upeer.upeerid)
    def getRoot(self):
        return self.root
    
    
    def makeSubGraph(self,uPeer,Graph,Visited):
        print uPeer.getName()
        for subPeer in uPeer.getPeers():
            Graph.add_node(subPeer.getName())
            Graph.add_edge(uPeer.getName(),subPeer.getName())
        for up in uPeer.getUpeers():
            if up != []:
                print Visited
                print up.getName()
                if up.getName() in Visited:
                    pass
                else:
                    print " ", up.getName()
                    Graph.add_node(up.getName())
                    Graph.add_edge(uPeer.getName(),up.getName())
                    Visited.append(uPeer.getName())
                    self.makeSubGraph(up,Graph,Visited)

    def makeGraph(self,Graph):
        Graph.add_node(self.root.getName())
        visited = []
        self.makeSubGraph(self.root,Graph,visited)

    

if __name__ == '__main__':
    # create a network and add 10 additional nodes
    n = Network()
    names = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']
    for i in range(10):
        n.newNode(names[i])   
    
    G = pgv.AGraph()
    n.makeGraph(G)
    G.layout()
    G.draw('file.png')
    sys.exit(0)
'''    G.add_nodes_from(['A','B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K'])
 root = n.getRoot()
    for i in root.getUpeers():
        G.add_edge(root.getName(),i.getName())
        for a in root.getPeers():
            G.add_edge(root.getName(),a.getName())
        for j in i.getUpeers():
            G.add_edge(i.getName(),j.getName())
            for k in j.getPeers():
                G.add_edge(j.getName(),k.getName())'''
   
