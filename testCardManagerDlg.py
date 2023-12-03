import sys
import os
import wx

import FlashCard
import AutoCorr
import CardManagerDlg as cm

# Define runtime path
runtimepath = os.getcwd()
print(runtimepath)

# Create a FlashCard set and generate test data
set = FlashCard.FlashCardSet()
set.GenerateTestData()
set.SelectChapter(0)

# Load auto correction settings
filename = os.path.join(runtimepath, 'test', 'autocorr.xml')
ac = AutoCorr.AutoCorr()
ac.Load(filename)

# Initialize the application
app = wx.App(False)

# Create and show the dialog
dlg = cm.CardManagerDlg(None, CardSet=set, filename='test.ofc', Config=None, autocorr=ac, help=None, runtimepath=runtimepath)
dlg.ShowModal()
dlg.Destroy()

# Start the application's main loop
app.MainLoop()

# Close the FlashCard set
set.Close()
