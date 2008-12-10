import sys, os, os.path
import wx

sys.path.append('../')
import FlashCard
import AutoCorr
import ChapterManagerDlg as cm

wd = os.getcwd()
runtimepath = os.path.dirname(wd)
print runtimepath

set = FlashCard.FlashCardSet()
set.GenerateTestData()
set.SelectChapter(0)

app = wx.PySimpleApp()

dlg = cm.ChapterManagerDlg(None, CardSet=set)
dlg.ShowModal()
dlg.Destroy()

app.MainLoop()

set.Close()
