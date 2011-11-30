#this code will be the backbone of every node's communication

import sys
import pickle

from flask import Flask
from flask import request, send_from_directory

app = Flask(__name__)

#--Node Receive Search Request--
#Ex: curl -d "filename=wat.txt&search_id=1" http://localhost:5000/search
@app.route("/search",methods=['POST'])
def search():
    searchreq=request.form['searchreq']
    
    searchreq=pickle.loads(str(searchreq))
    
    if(searchreq.requestor is None):
        searchreq.requestor=request.remote_addr
    
    return searchreq.requestor + " is searching (" + str(searchreq.searchid) + ", " + searchreq.filename+")"

#--Node Receive Download Request--
#Ex: curl http://localhost:5000/share/wat.txt
@app.route("/share/<filename>")
def getfile(filename):
    return send_from_directory('share',filename)

#--Client Receive Search Result--
#Ex: curl -d "path=share/wat.txt&search_id=1" http://localhost:5000/result
@app.route("/result",methods=['POST'])
def result():
    search_id=request.form['search_id']
    path=request.form['path']
    ip=request.remote_addr
    url="http://"+ip+":5000/"+path
    #add url/ip to list of results
    #handleResult(url)
    return url

#if __name__ == "__main__":
#    app.run(host='127.0.0.1', debug=True)
