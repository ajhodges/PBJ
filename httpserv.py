''' PBJ
    Camden Clements
    Adam Hodges
    Zach Welch
    
    httpserv.py handles flask and http calls for getting information
'''

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


@app.route("/search",methods=['POST'])
def search():
    '''
    --Node Receive Search Request--
    Ex: curl -d "filename=wat.txt&search_id=1" http://localhost:5000/search
    '''
    searchreq=request.form['searchreq']
    
    searchreq=pickle.loads(str(searchreq))
    
    if(searchreq.requestor is None):
        searchreq.requestor=request.remote_addr
    app.logger.debug(searchreq.requestor + " is searching (" + str(searchreq.searchid) + ", " + searchreq.filename+")")

    thr=threading.Thread(target=app.client.handleSearch, args=(searchreq,))
    thr.start()

    return searchreq.requestor + " is searching (" + str(searchreq.searchid) + ", " + searchreq.filename+")"

@app.route("/share/<filename>")
def getfile(filename):
    '''
    --Node Receive Download Request--
    Ex: curl http://localhost:5000/share/wat.txt
    '''
    return send_from_directory(app.client.share,filename)

@app.route("/result",methods=['POST'])
def result():
    '''
    --Client Receive Search Result--
    Ex: curl -d "path=share/wat.txt&search_id=1" http://localhost:5000/result
    '''
    result = request.form['result']
    result = pickle.loads(str(result))
    path = result.path
    print "%i hops this time." % result.hops
    ip=request.remote_addr
    url="http://"+ip+":"+request.form['port']+"/share/"+path
    #add url/ip to list of results
    
    if(app.window is not None):
        app.window.updateResult(url)
    return url

@app.route("/imapeer", methods=['GET'])
def regPeer():
    '''
    --UPeer Notified Of A Peer--
    add request.remote_addr as a connected peer
    '''
    app.client.addPeer(request.remote_addr+":"+request.args.get('port'))
    return "OK!"
    

@app.route("/imaupeer", methods=['GET'])
def regUPeer():
    '''
    --UPeer Notified Of Another UPeer--
    add request.remote_addr as a connected upeer
    '''
    app.client.addUPeer(request.remote_addr + ":"+ request.args.get('port'))
    return "OK!"


@app.route("/ping", methods=['GET'])
def ping():
    '''
    --UPeer Notified Of Another UPeer--
    add request.remote_addr as a connected upeer
    '''
    return "OK!"

def run(obsClient, obsWindow=None):
    import logging
    hdlr=logging.FileHandler('flask.log')
    app.logger.addHandler(hdlr)
    app.client=obsClient
    app.window=obsWindow
    app.run(host='0.0.0.0', port=obsClient.port)
    
