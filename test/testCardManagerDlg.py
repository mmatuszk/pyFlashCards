import sys, os, os.path
import wx

sys.path.append('../')
import FlashCard
import CardManagerDlg as cm

wd = os.getcwd()
runtimepath = os.path.dirname(wd)
print runtimepath

set = FlashCard.FlashCardSet()
set.GenerateTestData()
set.SelectChapter(0)

app = wx.PySimpleApp()

dlg = cm.CardManagerDlg(None, CardSet=set, Config=None, help=None, runtimepath=runtimepath)
dlg.ShowModal()
dlg.Destroy()

app.MainLoop()

set.Close()
