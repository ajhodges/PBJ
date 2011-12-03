# activate virtualenv
import os
activate_this = os.path.expanduser("env/bin/activate_this.py")
execfile(activate_this, dict(__file__=activate_this))

#import socket
import pickle
import sys
import math
import threading
import time

from flask import Flask
from flask import request
from httpcli import send_ping
app = Flask(__name__)

PEERS_PER_UPEER = 2
lock = threading.Lock()
class Node:
    def __init__(self, name, ultraId):
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
    def __init__(self):
        self.upeerCount = -1
        self.upeers = {}
        self.root = None
        self.outOfOrder = 0

    def findUPeer(self):
        for peer in self.upeers.values():
            print peer.peers
            if(len(peer.peers.keys()) < PEERS_PER_UPEER):
                if self.outOfOrder == 0:                 
                    return up

    def linkUPeer(self, up):
     
        for id,curup in self.upeers:
            if(math.log(math.abs((up.upeerid - curup.upeerid)), 2) % 2 == 0):
                print "Linking ultrapeers %d and %d." % (curup.upeerid, up.upeerid)
                up.upeers[curup.name] = curup
                curup.upeers[up.name] = up


  
    def addPeer(self, name):
        result = {}
        lock.acquire()
        if self.root == None:
            self.upeerCount += 1
            result['isUltra'] = True
            result['uPeers'] = None
            newNode = Node(name, self.upeerCount)
            self.root = newNode
            self.upeers[self.upeerCount] = newNode
            print "Node %s added to network as Ultrapeer %d." % (name, len(self.upeers))
            lock.release()
            return result
        else:    
            upeer = self.findUPeer(self.root)
            if upeer is None:
                result['isUltra'] = True
                self.upeerCount += 1
                if  self.upeersOutOfOrder != 0:
                    for i in range(self.upeerCount):
                        if self.upeers.has_key(i):
                            self.upeersOutOfOrder -= 1
                            newNode = Node(name, i)
                            self.upeers[i]= newNode
                            self.linkUPeer(newNode)
                            result['uPeers'] = newNode.upeers.keys()
                            print "Node %s added to network as Ultrapeer %d." % (name, len(self.upeers))
                            lock.release()
                            return result
                


            
                newNode = Node(name, self.upeerCount)
                self.upeers[self.upeerCount]= newNode
                self.linkUPeer(newNode)
                result['uPeers'] = newNode.upeers.keys()
                print "Node %s added to network as Ultrapeer %d." % (name, len(self.upeers))
                lock.release()
                return result
                
            else:
                newNode = Node(name, -1)
                newNode.upeer = upeer
                upeer.peers[name] = newNode
                print upeer.peers
                result['isUltra'] = False
                result['uPeer'] = upeer.name
                print "Node %s added to network under Ultrapeer %s" % (name, upeer.upeerid)
                lock.release()
                return result
    def pingify(self):
        while True:
            time.sleep(5)
            lock.acquire()
            for id,up in self.upeers.items():
                if send_ping(up.name) == False:
                    del self.upeers[id]
                    self.upeersOutOfOrder += 1
                    self.upeerCount -= 1
	    lock.release()	        

#def main():
#    pbj = Network()
#
#    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#    sock.bind(('', 5555))
#    sock.listen(1)    
#    while True:
#        conn, addr = sock.accept()threading.unlock()
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
    t = threading.Thread(target = pbj.pingify)
    t.start()
	
    app.run(host='0.0.0.0', debug=True)	
    



    #main()
