import wx
import wx.html
from wx.tools import helpviewer
import os

app=wx.PySimpleApp()
# Add the Zip filesystem
wx.FileSystem.AddHandler(wx.ZipFSHandler())
help = wx.html.HtmlHelpController()
help.SetTempDir(os.getcwd())
help.AddBook('help.zip', 1)
help.DisplayContents()
app.MainLoop()
