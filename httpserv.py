# activate virtualenv
import os
activate_this = os.path.expanduser("env/bin/activate_this.py")
execfile(activate_this, dict(__file__=activate_this))

#this code will be the backbone of every node's communication

import sys
import pickle

from flask import Flask
from flask import request, send_from_directory

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
    app.client.handleSearch(searchreq)

#--Node Receive Download Request--
#Ex: curl http://localhost:5000/share/wat.txt
@app.route("/share/<filename>")
def getfile(filename):
    return send_from_directory('share',filename)

#--Client Receive Search Result--
#Ex: curl -d "path=share/wat.txt&search_id=1" http://localhost:5000/result
@app.route("/result",methods=['POST'])
def result():
    path=request.form['path']
    ip=request.remote_addr
    url="http://"+ip+":5000/"+path
    #add url/ip to list of results
    frame.updateResult(url)
    return url

#--UPeer Notified Of A Peer--
@app.route("/imapeer", methods=['GET'])
def register():
    #add request.remote_addr as a connected peer
    app.client.addPeer(request.remote_addr)
    return "OK!"
    
#--UPeer Notified Of Another UPeer--
@app.route("/imaupeer", methods=['GET'])
def register():
    #add request.remote_addr as a connected upeer
    app.client.addUPeer(request.remote_addr)
    return "OK!"

def run(obsClient):
    import logging
    hdlr=logging.FileHandler('flask.log')
    app.logger.addHandler(hdlr)
    app.client=obsClient
    app.run(host='0.0.0.0')

if __name__ == "__main__":
    run()
