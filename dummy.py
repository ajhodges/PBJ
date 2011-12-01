# activate virtualenv
import os, time
activate_this = os.path.expanduser("env/bin/activate_this.py")
execfile(activate_this, dict(__file__=activate_this))

from pbj import Client
import httpserv

import threading

if __name__ == '__main__':
    client = Client()
    client.connectToNetwork()
    httpserv.run(client)

