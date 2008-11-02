import sys, os, os.path
import wx

sys.path.append('../')
import FlashCard
import AutoCorr
import TextHtmlCtrl

class TestFrame(wx.Frame):
    def __init__(self, parent, id, autocorr):
        wx.Frame.__init__(self, parent, id, "Test TextHtmlCtrl", size=(400,300))

        sizer = wx.BoxSizer(wx.VERTICAL)

        thc = TextHtmlCtrl.TextHtmlCtrl(self, -1, autocorr, style=wx.TE_MULTILINE)

        sizer.Add(thc, 1, wx.EXPAND)

        self.SetSizer(sizer)

wd = os.getcwd()
runtimepath = os.path.dirname(wd)
print runtimepath

filename='autocorr.xml'

ac = AutoCorr.AutoCorr()
ac.Load(filename)

app = wx.PySimpleApp()

win = TestFrame(None, -1, ac)
win.Show()

app.MainLoop()

ac.Save(filename)

