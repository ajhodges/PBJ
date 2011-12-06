# activate virtualenv
import os
activate_this = os.path.expanduser("env/bin/activate_this.py")
execfile(activate_this, dict(__file__=activate_this))

#this code will be the backbone of every node's communication

import sys
import pickle

from flask import Flask
from flask import request, send_from_directory

import threading

app = Flask(__name__)

app.client = None

#--Node Receive Search Request--
#Ex: curl -d "filename=wat.txt&search_id=1" http://localhost:5000/search
@app.route("/search",methods=['POST'])
def search():
    searchreq=request.form['searchreq']
    
    searchreq=pickle.loads(str(searchreq))
    
    if(searchreq.requestor is None):
        searchreq.requestor=request.remote_addr
    app.logger.debug(searchreq.requestor + " is searching (" + str(searchreq.searchid) + ", " + searchreq.filename+")")

    thr=threading.Thread(target=app.client.handleSearch, args=(searchreq,))
    thr.start()

    return searchreq.requestor + " is searching (" + str(searchreq.searchid) + ", " + searchreq.filename+")"

#--Node Receive Download Request--
#Ex: curl http://localhost:5000/share/wat.txt
@app.route("/share/<filename>")
def getfile(filename):
    return send_from_directory(app.client.share,filename)

#--Client Receive Search Result--
#Ex: curl -d "path=share/wat.txt&search_id=1" http://localhost:5000/result
@app.route("/result",methods=['POST'])
def result():
    path=request.form['path']
    ip=request.remote_addr
    url="http://"+ip+":5000/share/"+path
    #add url/ip to list of results
    
    if(app.window is not None):
        app.window.updateResult(url)
    return url

#--UPeer Notified Of A Peer--
@app.route("/imapeer", methods=['GET'])
def regPeer():
    #add request.remote_addr as a connected peer
    app.client.addPeer(request.remote_addr)
    return "OK!"
    
#--UPeer Notified Of Another UPeer--
@app.route("/imaupeer", methods=['GET'])
def regUPeer():
    #add request.remote_addr as a connected upeer
    app.client.addUPeer(request.remote_addr)
    return "OK!"

#--UPeer Notified Of Another UPeer--
@app.route("/ping", methods=['GET'])
def ping():
    #add request.remote_addr as a connected upeer
    return "OK!"

def run(obsClient, obsWindow=None):
    import logging
    hdlr=logging.FileHandler('flask.log')
    app.logger.addHandler(hdlr)
    app.client=obsClient
    app.window=obsWindow
    app.run(host='0.0.0.0')
    
