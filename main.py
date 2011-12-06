''' PBJ
    Camden Clements
    Adam Hodges
    Zach Welch
    
    main.py executes client code and handles GUI
'''

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

        # layout components
        self.panel = wx.Panel(self, -1)
        self.control = wx.BoxSizer(wx.VERTICAL)

        # create self.searchbar
        self.createSearchBar()

        #create listbox to store results
        self.resultsarea = wx.ListBox(self.panel, size=(350,200))
        self.downloadb = wx.Button(self.panel, label="Download")
        self.downloadb.SetToolTip(wx.ToolTip('Save selected file to /share/'))
        self.downloadb.Bind(wx.EVT_BUTTON, self.download)

        #put search bar on top of listbox
        self.control.AddSpacer((0,5))
        self.control.Add(self.searchbar, 0, wx.ALIGN_CENTRE)
        self.control.AddSpacer((0,5))
        self.control.Add(self.resultsarea, 0, wx.ALIGN_CENTRE)
        self.control.Add(self.downloadb, 0, wx.ALIGN_CENTRE)
        self.control.AddSpacer((0,10))
        
        self.panel.SetSizer(self.control)

        self.CreateStatusBar() # A Statusbar in the bottom of the window

        self.Show(True)

        # set size
        self.control.Fit(self)
        self.SetSize((400, 300))
        self.SetMinSize((400,300))
    
    def createSearchBar(self):
        # Horizontal sizer
        self.searchbar = wx.BoxSizer(wx.HORIZONTAL)

        self.text = wx.StaticText(self.panel, label="Search:")
        self.inputarea = wx.TextCtrl(self.panel, size=wx.Size(250, -1))
        self.button = wx.Button(self.panel, label="Go")
        self.button.Bind(wx.EVT_BUTTON, self.search)

        #Add to horizontal sizer
        self.searchbar.Add(self.text, 0,)
        self.searchbar.AddSpacer((5,0))
        self.searchbar.Add(self.inputarea, 1)
        self.searchbar.AddSpacer((5,0))
        self.searchbar.Add(self.button, 0)

    def search(self, event):
        client.search(self.inputarea.GetValue())

    def download(self, event):
        if(self.resultsarea.GetSelection() != -1):
            client.download(self.resultsarea.GetString(self.resultsarea.GetSelection()))
        
    def setStatus(self, text):
        #wx.MutexGuiEnter()
        self.SetStatusText(text)
        #wx.MutexGuiEnter()
        
    def updateResult(self, url):
        wx.MutexGuiEnter()
        self.resultsarea.Append(url)
        wx.MutexGuiLeave()

#class runWindow(threading.Thread):
#    def __init__(self, app):
#        threading.Thread.__init__(self)
#        self.app = app
#    def run(self):
#        print "here"
#        self.app.MainLoop()

class runClient(threading.Thread):
    def __init__(self, client, frame):
        threading.Thread.__init__(self)
        self.client = client
        self.frame = frame
    def run(self):
        httpserv.run(self.client, self.frame)

def main():
    app = wx.App(False)
    frame = MainWindow(None, "PBJ")
    client.connectToNetwork()
    frame.setStatus("Connected to " + str(client.getUpeers()))
    #t=runWindow(app)
    #t.start()
    c = runClient(client, frame)
    c.start()
    #httpserv.run(client, frame)
    app.MainLoop()

if __name__ == '__main__':
    main()
