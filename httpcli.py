''' PBJ
    Camden Clements
    Adam Hodges
    Zach Welch
    
    httpcli.py handles http calls for sending information
'''
# activate virtualenv
import os
activate_this = os.path.expanduser("env/bin/activate_this.py")
execfile(activate_this, dict(__file__=activate_this))

#these are methods that are used to communicate with other nodes or a gateway

import urllib
import urllib2
import pickle
GATEWAY_ADDR = '10.125.3.145'


def send_ping(node):
    '''called by peer to register with ultrapeer'''
    url="http://"+node+"/ping"
    try:
        req=urllib2.Request(url)
        response=urllib2.urlopen(req)
        return True
    except Exception:
        return False


def send_register(myport, gateway):
    '''called by node to register with gateway, returns pickle obj'''
    url="http://"+gateway+":5000/register?port="+myport
    req=urllib2.Request(url)
    response=urllib2.urlopen(req)
    return(response.read())
    

def send_imapeer(myport, upeer):
    '''called by peer to register with ultrapeer'''
    url="http://"+upeer+"/imapeer?port="+myport
    try:
        req=urllib2.Request(url)
        response=urllib2.urlopen(req)
        return True
    except Exception:
        return False


def send_imaupeer(myport, upeer):
    '''called by ultrapeer to register with another ultrapeer'''
    url="http://"+upeer+"/imaupeer?port="+myport
    try:
        req=urllib2.Request(url)
        response=urllib2.urlopen(req)
        return True
    except Exception:
        return False

def send_tellsearch(searchterm, peer):
    url="http://"+peer+"/tellsearch"
    values={'searchterm':searchterm}
    data=urllib.urlencode(values)
    req=urllib2.Request(url,data)
    response=urllib2.urlopen(req)


def send_search(searchreq, superpeerip):
    '''used to initiate/propagate a search request'''
    url="http://"+superpeerip+"/search"
    values={'searchreq':pickle.dumps(searchreq)}
    
    data=urllib.urlencode(values)
    req=urllib2.Request(url,data)
    response=urllib2.urlopen(req)
    #print(response.read())



def send_found(port, request):
    '''called by node if the file has been found'''
    url="http://"+request.requestor+":"+request.requestorport+"/result"
    values={'result':pickle.dumps(request), 'port':port}

    data=urllib.urlencode(values)
    req=urllib2.Request(url,data)
    response=urllib2.urlopen(req)
    #print(response.read())


def download(filename, url, dlpath):
    '''called by client after it has a list of results to finally download the file'''
    req=urllib2.Request(url)
    response=urllib2.urlopen(req)
    
    #write the file to the share folder
    download = open(dlpath+'/'+filename, "w")
    download.write(response.read())
    download.close()
    

def send_gateway_remove_peer(p):
    '''called by ultrapeer to u'''
    url="http://"+GATEWAY_ADDR+":5000/upeer_remove_peer"
    values={'peer':p}
    data=urllib.urlencode(values)
    req=urllib2.Request(url,data)
    response=urllib2.urlopen(req)

#def main():
    #--testing functions--
    #send_search(pbj.searchReq(1,"wat.txt"), "localhost")
    #report_found(1,"hold.txt", "localhost")
    #download("hold.txt", "http://127.0.0.1:5000/share/hold.txt")
    #register("localhost")

#if __name__ == "__main__":
#    main()
