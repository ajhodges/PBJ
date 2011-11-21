#!/usr/bin/env python
import wx

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(500,400))
        self.control = wx.SplitterWindow(self, style=wx.SP_BORDER)

        #create splitter with search box + button
        searchbar = wx.SplitterWindow(self.control, style=wx.SP_NOBORDER)

        inputarea = wx.TextCtrl(searchbar, style=wx.TE_PROCESS_ENTER)
        button = wx.Button(searchbar, label="Go")
        searchbar.SplitVertically(inputarea, button, -40)

        #create listbox to store results
        resultsarea = wx.ListBox(self.control)

        #put search bar on top of listbox
        self.control.SplitHorizontally(searchbar, resultsarea, 30)

        self.CreateStatusBar() # A Statusbar in the bottom of the window

        self.Show(True)

app = wx.App(False)
frame = MainWindow(None, "PBJ")
app.MainLoop()
