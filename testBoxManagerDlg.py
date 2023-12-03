import sys

import os

import wx
from FlashCard import FlashCardSet  # Assuming FlashCardSet is in the FlashCard module
from BoxManagerDlg import *

class TestBoxManagerApp(wx.App):
    def OnInit(self):
        # Create a FlashCardSet instance and populate it with test data
        card_set = FlashCardSet()
        card_set.GenerateTestData()

        # Optionally, you can perform operations on the set
        card_set.SelectChapter(0)

        # Now, create and show the BoxManagerDlg using the test data
        dlg = BoxManagerDlg(None, card_set)
        dlg.ShowModal()
        dlg.Destroy()
        return True

if __name__ == '__main__':
    app = TestBoxManagerApp(redirect=False)
    app.MainLoop()