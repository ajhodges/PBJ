# activate virtualenv
import os, sys
activate_this = os.path.expanduser("env/bin/activate_this.py")
execfile(activate_this, dict(__file__=activate_this))

from pbj import Client
import httpserv

import threading

if __name__ == '__main__':
    if(len(sys.argv)==2):
        client = Client(sys.argv[1])
    else:
        client = Client()
    client.connectToNetwork()
    httpserv.run(client)

