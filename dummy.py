# activate virtualenv
import os
activate_this = os.path.expanduser("env/bin/activate_this.py")
execfile(activate_this, dict(__file__=activate_this))

from multiprocessing import Process
from pbj import Client

client = Client()

def main():
    client.connectToNetwork()
    
    httpserv.app.run(host='0.0.0.0', debug=True)
    

if __name__ == '__main__':
    main()
