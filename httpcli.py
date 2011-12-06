''' PBJ
    Camden Clements
    Adam Hodges
    Zach Welch
    
    httpcli.py handles flask and http calls for sending information
'''
# activate virtualenv
import os
activate_this = os.path.expanduser("env/bin/activate_this.py")
execfile(activate_this, dict(__file__=activate_this))

#these are methods that are used to communicate with other nodes or a gateway

import urllib
import urllib2
import pickle
GATEWAY_ADDR = 'gecko22.cs.clemson.edu'


def send_ping(node):
    '''called by peer to register with ultrapeer'''
    url="http://"+node+":5000/ping"
    try:
        req=urllib2.Request(url)
        response=urllib2.urlopen(req)
        return True
    except Exception:
        return False


def send_register(gateway):
    '''called by node to register with gateway, returns pickle obj'''
    url="http://"+gateway+":5000/register"
    req=urllib2.Request(url)
    response=urllib2.urlopen(req)
    return(response.read())
    

def send_imapeer(upeer):
    '''called by peer to register with ultrapeer'''
    url="http://"+upeer+":5000/imapeer"
    try:
        req=urllib2.Request(url)
        response=urllib2.urlopen(req)
        return True
    except Exception:
        return False


def send_imaupeer(upeer):
    '''called by ultrapeer to register with another ultrapeer'''
    url="http://"+upeer+":5000/imaupeer"
    try:
        req=urllib2.Request(url)
        response=urllib2.urlopen(req)
        return True
    except Exception:
        return False
    

def send_search(searchreq, superpeerip):
    '''used to initiate/propagate a search request'''
    url="http://"+superpeerip+":5000/search"
    values={'searchreq':pickle.dumps(searchreq)}
    
    data=urllib.urlencode(values)
    req=urllib2.Request(url,data)
    response=urllib2.urlopen(req)
    #print(response.read())


def send_found(requestor, path):
    '''called by node if the file has been found'''
    url="http://"+requestor+":5000/result"
    values={'path':path}
    data=urllib.urlencode(values)
    req=urllib2.Request(url,data)
    response=urllib2.urlopen(req)
    #print(response.read())


def download(filename, url):
    '''called by client after it has a list of results to finally download the file'''
    req=urllib2.Request(url)
    response=urllib2.urlopen(req)
    
    #write the file to the share folder
    download = open('share/'+filename, "w")
    download.write(response.read())
    download.close()
    

def send_gateway_remove_peer(p):
    '''called by ultrapeer to u'''
    url="http://"+GATEWAY_ADDR+":5000/upeer_remove_peer"
    values={'peer':p}
    data=urllib.urlencode(values)
    req=urllib2.Request(url,data)
    response=urllib2.urlopen(req)

def main():
    #--testing functions--
    send_search(pbj.searchReq(1,"wat.txt"), "localhost")
    #report_found(1,"hold.txt", "localhost")
    #download("hold.txt", "http://127.0.0.1:5000/share/hold.txt")
    #register("localhost")

if __name__ == "__main__":
    main()
