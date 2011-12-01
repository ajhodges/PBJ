# activate virtualenv
import os, time
activate_this = os.path.expanduser("env/bin/activate_this.py")
execfile(activate_this, dict(__file__=activate_this))

from pbj import Client
import httpserv

import threading

client = Client()
def runClient():
    client.connectToNetwork()


if __name__ == '__main__':
	server=threading.Thread(target=runClient)
	server.start()
	httpserv.run()

