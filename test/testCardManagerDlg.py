import sys, os, os.path
import wx

sys.path.append('../')
import FlashCard
import AutoCorr
import CardManagerDlg as cm

wd = os.getcwd()
runtimepath = os.path.dirname(wd)
print runtimepath

set = FlashCard.FlashCardSet()
set.GenerateTestData()
set.SelectChapter(0)

filename=os.path.join(runtimepath, 'test', 'autocorr.xml')
ac = AutoCorr.AutoCorr()
ac.Load(filename)

app = wx.PySimpleApp()

dlg = cm.CardManagerDlg(None, CardSet=set, Config=None, autocorr= ac, help=None, runtimepath=runtimepath)
dlg.ShowModal()
dlg.Destroy()

app.MainLoop()

set.Close()
