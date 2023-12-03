import sys

import wx
from FlashCard import FlashCardSet  # Assuming FlashCardSet is in the FlashCard module
from CardBrowserDlg import *
import configparser


class TestCardBrowserApp(wx.App):
    def OnInit(self):
        # Create a FlashCardSet instance and populate it with test data
        card_set = FlashCardSet()
        card_set.GenerateTestData()

        # Optionally, perform operations on the set
        card_set.SelectChapter(0)

        # Now, create and show the CardBrowserDlg using the test data
        # Assume you have a Config class or similar for configuration
        config = configparser.ConfigParser()
        # Create the section 'card_browser'
        config.add_section('card_browser')
        # set some default values
        config.set('card_browser', 'width', str(1024))
        config.set('card_browser', 'height', str(800))

        dlg = CardBrowserDlg(None, -1, card_set, config, title="Card Browser Test")
        dlg.ShowModal()
        dlg.Destroy()
        return True

if __name__ == '__main__':
    app = TestCardBrowserApp(redirect=False)
    app.MainLoop()