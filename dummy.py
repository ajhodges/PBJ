#!/usr/bin/env python
from multiprocessing import Process
from pbj import Client

client = Client()

def main():
    client.connectToNetwork()
    
    server = Process(target=runServer)
    
    app.MainLoop()

def runServer():
    httpserv.app.run(host='0.0.0.0', debug=True)

if __name__ == '__main__':
    main()
