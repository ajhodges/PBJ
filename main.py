# activate virtualenv
import os
activate_this = os.path.expanduser("env/bin/activate_this.py")
execfile(activate_this, dict(__file__=activate_this))

import wx
from pbj import Client

import threading

import httpserv

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

app = wx.App(False)
frame = MainWindow(None, "PBJ")
frame.setStatus("Connected to " + str(client.getUpeers()))

def runWindow():
    app.MainLoop()

def main():
    client.connectToNetwork()
    t=threading.Thread(target=runWindow)
    t.start()
    httpserv.run(client, frame)

if __name__ == '__main__':
    main()
