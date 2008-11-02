import sys, os, os.path
import wx

sys.path.append('../')
import FlashCard
import AutoCorrDlg as acdlg
import AutoCorr

wd = os.getcwd()
runtimepath = os.path.dirname(wd)
print runtimepath

filename='autocorr.xml'

ac = AutoCorr.AutoCorr()
ac.Load(filename)

app = wx.PySimpleApp()

dlg = acdlg.AutoCorrDlg(None, -1, ac)
dlg.ShowModal()
dlg.Destroy()

app.MainLoop()

ac.Save(filename)
