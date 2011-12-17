''' PBJ
    Camden Clements
    Adam Hodges
    Zach Welch
    
    gateway.py contains code for the PBJ gateway, which controls how nodes are
    added to the network
'''
# activate virtualenv
import os
activate_this = os.path.expanduser("env/bin/activate_this.py")
execfile(activate_this, dict(__file__=activate_this))

import pickle
import sys
import math
import threading
import time
import getopt

from flask import Flask
from flask import request
from httpcli import send_ping
app = Flask(__name__)

PEERS_PER_UPEER = 2

class Node:
    '''gateway representation of a network node'''
    def __init__(self, name, ultraId):
        '''constructor 
           name    - IP address of node
           ultraId - ultra peer ID number (-1 if not an ultra peer)
        '''
        self.name = name
        if ultraId == -1:
            self.isUltra = False
            self.upeer = None
        else:
            self.isUltra = True
            self.upeerid = ultraId
            self.peers = {}
            self.upeers = {}

class Network:
    '''gateway representation of entire network'''
    def __init__(self):
        '''constructor, sets up empty network'''
        self.upeerCount = -1
        self.upeers = {}
        self.outOfOrder = 0

    def findUPeer(self):
        '''returns the ultra peer with an empty sub network slot or None if all ultra peers are full'''
        for peer in self.upeers.values():
            if(len(peer.peers.keys()) < PEERS_PER_UPEER):
                if self.outOfOrder == 0:                 
                    return peer

    def linkUPeer(self, up):
        '''links a ultra peer to all other ultra peers it should be linked with'''
        for ids,curup in self.upeers.items():
            if(up.upeerid - curup.upeerid != 0):
                if(math.log(math.fabs((up.upeerid - curup.upeerid)), 2) % 2 == 0):
                    print "Linking ultrapeers %d and %d." % (curup.upeerid, up.upeerid)
                    up.upeers[curup.name] = curup
                    curup.upeers[up.name] = up
  
    def addPeer(self, name):
        '''process for adding a peer to the network. Checks network for lost nodes
            before adding new ones
            name - ip address of new node to be added 
        '''
        result = {}

        # ping ultrapeers to verify network
        for id,up in self.upeers.items():
            if send_ping(up.name) == False:
                print "Lost Ultrapeer ", id
                del self.upeers[id]
                self.outOfOrder += 1
                self.upeerCount -= 1

        upeer = self.findUPeer()
        if upeer is None:
            # new peer is ultra peer
            result['isUltra'] = True
            self.upeerCount += 1
            
            # adjust ultrapeers
            if  self.outOfOrder != 0:
                self.outOfOrder -= 1
                for i in range(self.upeerCount):
                    if self.upeers.has_key(i) == False:
                        newNode = Node(name, i)
                        self.upeers[i]= newNode
                        self.linkUPeer(newNode)
                        result['uPeers'] = newNode.upeers.keys()
                        result['upId'] = newNode.upeerid
                        print "Node %s added to network as Ultrapeer %d." % (name, newNode.upeerid)
                        return result
            # put new upeer at end of upeers
            newNode = Node(name, self.upeerCount)
            self.upeers[self.upeerCount]= newNode
            self.linkUPeer(newNode)
            result['uPeers'] = newNode.upeers.keys()
            result['upId'] = newNode.upeerid
            print "Node %s added to network as Ultrapeer %d." % (name, newNode.upeerid)

            return result
            
        else:
            # new peer is not an ultra peer
            newNode = Node(name, -1)
            newNode.upeer = upeer
            upeer.peers[name] = newNode
            result['isUltra'] = False
            result['uPeer'] = upeer.name
            print "Node %s added to network under Ultrapeer %s" % (name, upeer.upeerid)

            return result
            
    def UPeerRemovePeer(self, upeer, peer):
        '''method for removing peer from a upeers sub network'''
        for ids,up in self.upeers.items():
            if(up.name==upeer):
                del up.peers[peer]
        #set upeer's count to count

pbj = Network()
@app.route("/register", methods=['GET'])
def register():
    '''flask method that new nodes use to register with the network'''
    data=pbj.addPeer(request.remote_addr)
    return pickle.dumps(data)
    
@app.route("/upeer_remove_peer", methods=['POST'])
def updatePeerCount():
    '''flask method that ultranodes use to tell gateway they have lost a node'''
    peer=request.form['peer']
    upeer=request.remote_addr
    pbj.UPeerRemovePeer(upeer, peer)
    return "OK"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)    
