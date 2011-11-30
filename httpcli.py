#these are methods that are used to communicate with other nodes or a gateway

import urllib
import urllib2
import pickle


#called by node to register with gateway, returns pickle obj
def send_register(gateway):
    url="http://"+gateway+":5000/register"
    req=urllib2.Request(url)
    response=urllib2.urlopen(req)
    
    return(response.read())
    
#used to initiate/propagate a search request
def send_search(searchreq, superpeerip):
    url="http://"+superpeerip+":5000/search"
    values={'searchreq':pickle.dumps(searchreq)}
    
    data=urllib.urlencode(values)
    req=urllib2.Request(url,data)
    response=urllib2.urlopen(req)
    print(response.read())

#called by node if the file has been found
def send_found(requestor, path):
    url="http://"+requestor+":5000/result"
    values={'path':path}
    data=urllib.urlencode(values)
    req=urllib2.Request(url,data)
    response=urllib2.urlopen(req)
    #print(response.read())

#called by client after it has a list of results to finally download the file
def download(filename, url):
    req=urllib2.Request(url)
    response=urllib2.urlopen(req)
    
    #write the file to the share folder
    download = open('share/'+filename, "w")
    download.write(response.read())
    download.close()

def main():
    #--testing functions--
    send_search(pbj.searchReq(1,"wat.txt"), "localhost")
    #report_found(1,"hold.txt", "localhost")
    #download("hold.txt", "http://127.0.0.1:5000/share/hold.txt")
    #register("localhost")

if __name__ == "__main__":
    main()
