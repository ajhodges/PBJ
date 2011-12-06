''' PBJ
    Camden Clements
    Adam Hodges
    Zach Welch
    
    gateway_test.py
'''

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
import getopt

import wx

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
        self.outOfOrder = 0

    def findUPeer(self):
        for peer in self.upeers.values():
            if(len(peer.peers.keys()) < PEERS_PER_UPEER):
                if self.outOfOrder == 0:                 
                    return peer

    def linkUPeer(self, up):
     
        for ids,curup in self.upeers.items():
            if(up.upeerid - curup.upeerid != 0):
                if(math.log(math.fabs((up.upeerid - curup.upeerid)), 2) % 2 == 0):
                    print "Linking ultrapeers %d and %d." % (curup.upeerid, up.upeerid)
                    up.upeers[curup.name] = curup
                    curup.upeers[up.name] = up


  
    def addPeer(self, name):
        print "ADDING A PEEEEEEEEEEEEEEEEEEEERR"
        result = {}
        for id,up in self.upeers.items():
            if send_ping(up.name) == False:
                print "Lost Ultrapeer ", id
                del self.upeers[id]
                self.outOfOrder += 1
                self.upeerCount -= 1


        upeer = self.findUPeer()
        if upeer is None:
            result['isUltra'] = True
            self.upeerCount += 1
            if  self.outOfOrder != 0:
                self.outOfOrder -= 1
                for i in range(self.upeerCount):
                    if self.upeers.has_key(i) == False:
                        print "HERE 1"
                      
                        newNode = Node(name, i)
                        self.upeers[i]= newNode
                        self.linkUPeer(newNode)
                        result['uPeers'] = newNode.upeers.keys()
                        print "Node %s added to network as Ultrapeer %d." % (name, newNode.upeerid)

                        return result
            


            print "HERE2"
            newNode = Node(name, self.upeerCount)
            self.upeers[self.upeerCount]= newNode
            self.linkUPeer(newNode)
            result['uPeers'] = newNode.upeers.keys()
            print "Node %s added to network as Ultrapeer %d." % (name, newNode.upeerid)

            return result
            
        else:
            newNode = Node(name, -1)
            newNode.upeer = upeer
            upeer.peers[name] = newNode
            result['isUltra'] = False
            result['uPeer'] = upeer.name
            print "Node %s added to network under Ultrapeer %s" % (name, upeer.upeerid)

            return result
       
        G = pgv.AGraph()
        self.makeGraph(G)
        G.layout()
        G.draw('file.png')
            
    def UPeerRemovePeer(self, upeer, peer):
        for ids,up in self.upeers.items():
            if(up.name==upeer):
                del up.peers[peer]
        #set upeer's count to count

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

    def makeGraph(self,Graph):
        Graph.add_node(self.root.getName())
        visited = []
        self.makeSubGraph(self.root,Graph,visited)

pbj = Network()
@app.route("/register", methods=['GET'])
def register():
    data=pbj.addPeer(request.remote_addr)
    return pickle.dumps(data)
    
@app.route("/upeer_remove_peer", methods=['POST'])
def updatePeerCount():
    peer=request.form['peer']
    upeer=request.remote_addr
    pbj.UPeerRemovePeer(upeer, peer)
    return "OK"

class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title)
        self.bitmap = wx.Bitmap('file.png')
        wx.EVT_PAINT(self, self.OnPaint)
        self.Centre()
    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        dc.DrawBitmap(self.bitmap, 60, 20)

class displayApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, 'PBJ Network')
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

class display(threading.Thread):
    def __init__(self, app):
        threading.Thread.__init__(self)
        self.app = displayApp(0)
    def run(self):
        self.app.MainLoop()    

if __name__ == "__main__":
    
    options, remainder = getopt.getopt(sys.argv[1:], 'l:')
    for opt, arg in options:
        if opt in '-l':
            PEERS_PER_UPEER = arg
            print "Setting PEERS_PER_UPEER to " + arg
    a = display(app)
    a.start()
    app.run(host='0.0.0.0', port=5001, debug=True)    
    print 'q'
    #main()
