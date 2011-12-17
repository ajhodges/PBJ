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

class dummyClass:
    def __init__(self):
        self.csvwriter=csv.writer(open("results.csv", "wb"))

    def updateResult(self, url, searchresult):
        csvwriter.writerow([searchresult.searchid, searchresult.timeinit, time.time(), searchrequest.ttl, searchrequest.lastUltranode, url])

if __name__ == '__main__':
    '''Accept share directory path as an optional argument'''
    if(len(sys.argv)==2):
        client = Client(str(sys.argv[1]))
    else:
        client = Client()
        dummy = dummyClass()

    client.connectToNetwork()
    httpserv.run(client, obsDummy=dummy)

