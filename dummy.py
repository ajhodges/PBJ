''' PBJ
    Camden Clements
    Adam Hodges
    Zach Welch
    
    dummy.py excecutes a GUIless client, used for building a test network 
'''

# activate virtualenv
import os, sys
activate_this = os.path.expanduser("env/bin/activate_this.py")
execfile(activate_this, dict(__file__=activate_this))

from pbj import Client
import httpserv
import csv
import threading
import time
import socket

class dummyClass:
    def __init__(self, path):
        self.csvfile=path+'.csv'
    def updateResult(self, url, searchresult):
        file=open(self.csvfile, "at")
        self.csvwriter=csv.writer(file)
        self.csvwriter.writerow([searchresult.searchid, searchresult.timeinit, time.time(), searchresult.ttl, searchresult.lastUltranode, url])
        file.close()

if __name__ == '__main__':
    '''Accept share directory path as an optional argument'''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 0))
    port = sock.getsockname()[1]
    sock.close()

    port = str(port)

    if(len(sys.argv)==2):
        client = Client(str(sys.argv[1]), port)
    else:
        client = Client('share', port)

    dummy = dummyClass(str(sys.argv[1]))

    client.connectToNetwork()
    httpserv.run(client, obsDummy=dummy)

