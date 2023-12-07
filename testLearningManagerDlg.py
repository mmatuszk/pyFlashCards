import sys
import os
import wx
from FlashCard import FlashCardSet
import LearningManagerDlg as lm

# Get the runtime path
runtimepath = os.path.dirname(os.getcwd())
print(runtimepath)

# Create a FlashCardSet instance and generate test data
flashcard_set = FlashCardSet()
flashcard_set.GenerateTestData()
flashcard_set.SelectChapter(0)

# Initialize the application
app = wx.App(False)

# Create and show the LearningManagerDlg
dlg = lm.LearningManagerDlg(None, CardSet=flashcard_set, help=None, runtimepath=runtimepath)
dlg.ShowModal()
dlg.Destroy()

# Main event loop
app.MainLoop()

flashcard_set.Close()
