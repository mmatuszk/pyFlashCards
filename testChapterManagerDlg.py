import sys
import os
import wx
from FlashCard import FlashCardSet
import ChapterManagerDlg as cm

# Get the runtime path
runtimepath = os.path.dirname(os.getcwd())
print(runtimepath)

# Create a FlashCardSet instance and generate test data
flashcard_set = FlashCardSet()
flashcard_set.GenerateTestData()
flashcard_set.SelectChapter(0)

# Initialize the application
app = wx.App(False)

# Create and show the ChapterManagerDlg
dlg = cm.ChapterManagerDlg(None, CardSet=flashcard_set)
dlg.ShowModal()
dlg.Destroy()

# Main event loop
app.MainLoop()

flashcard_set.Close()
