# activate virtualenv
import os
activate_this = os.path.expanduser("env/bin/activate_this.py")
execfile(activate_this, dict(__file__=activate_this))

#import socket
import pickle
import sys
import math

from flask import Flask
from flask import request

app = Flask(__name__)

PEERS_PER_UPEER = 2

class Node:
    def __init__(self, name, ultraId):
        self.name = name
        if ultraId == 0:
            self.isUltra = False
            self.upeer = None
        else:
            self.isUltra = True
            self.upeerid = ultraId
            self.peers = {}
            self.upeers = {}

class Network:
    def __init__(self):
        self.peers = 0
        self.upeers = []
        self.root = None

    def findUPeer(self, up):
        print up.peers
        if(len(up.peers.keys()) < PEERS_PER_UPEER):
            return up
        else:
            for peer in up.upeers.values():
                if(peer.upeerid > up.upeerid):
                    return self.findUPeer(peer)

    def linkUPeer(self, up):
        for curup in self.upeers:
            if(curup == up):
                break
            elif(math.log((up.upeerid - curup.upeerid), 2) % 2 == 0):
                print "Linking ultrapeers %d and %d." % (curup.upeerid, up.upeerid)
                up.upeers[curup.name] = curup
                curup.upeers[up.name] = up

    def addPeer(self, name):
        self.peers += 1
        result = {}
        
        if self.root == None:
            result['isUltra'] = True
            result['uPeers'] = None
            newNode = Node(name, 1)
            self.root = newNode
            self.upeers.append(newNode)
            print "Node %s added to network as Ultrapeer %d." % (name, len(self.upeers))
            return result
        else:
            upeer = self.findUPeer(self.root)
            if upeer is None:
                result['isUltra'] = True
                newNode = Node(name, len(self.upeers) + 1)
                self.upeers.append( newNode)
                self.linkUPeer(newNode)
                result['uPeers'] = newNode.upeers.keys()
                print "Node %s added to network as Ultrapeer %d." % (name, len(self.upeers))
                return result
                
            else:
                newNode = Node(name, 0)
                newNode.upeer = upeer
                upeer.peers[name] = newNode
                print upeer.peers
                result['isUltra'] = False
                result['uPeer'] = upeer.name
                print "Node %s added to network under Ultrapeer %s" % (name, upeer.upeerid)
                return result

#def main():
#    pbj = Network()
#
#    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#    sock.bind(('', 5555))
#    sock.listen(1)    
#    while True:
#        conn, addr = sock.accept()
#        result = pbj.addPeer(addr[0])
#        result = pickle.dumps(result)
#        conn.send(result)
#        conn.close()

pbj = Network()
@app.route("/register", methods=['GET'])
def register():
    data=pbj.addPeer(request.remote_addr)
    return pickle.dumps(data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
    #main()
