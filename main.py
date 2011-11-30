#!/usr/bin/env python
import wx
from multiprocessing import Process
from pbj import Client

client = Client()

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(500,400))
        self.control = wx.SplitterWindow(self, style=wx.SP_BORDER)

        #create splitter with search box + button
        searchbar = wx.SplitterWindow(self.control, style=wx.SP_NOBORDER)

        self.inputarea = wx.TextCtrl(searchbar, style=wx.TE_PROCESS_ENTER)
        button = wx.Button(searchbar, label="Go")
        button.Bind(wx.EVT_BUTTON, self.search)
        
        searchbar.SplitVertically(self.inputarea, button, -40)

        #create listbox to store results
        self.resultsarea = wx.ListBox(self.control)

        #put search bar on top of listbox
        self.control.SplitHorizontally(searchbar, self.resultsarea, 30)

        self.CreateStatusBar() # A Statusbar in the bottom of the window

        self.Show(True)
    
    def search(self, event):
        client.search(self.inputarea.GetValue())
        
    def setStatus(self, text):
        self.SetStatusText(text)
        
    def updateResult(self, url):
        self.resultsarea.Append(url)

def main():
    client.connectToNetwork()
    
    server = Process(target=runServer)
    
    app = wx.App(False)
    frame = MainWindow(None, "PBJ")
    frame.setStatus("Connected to " + str(client.getUpeers()))
    app.MainLoop()

def runServer():
    httpserv.app.run(host='127.0.0.1', debug=True)

if __name__ == '__main__':
    main()
