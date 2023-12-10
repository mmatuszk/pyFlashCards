# testExportWizard.py
import wx
import wx.adv as adv
import ExportCSVWizard
import FlashCard
import os, os.path
import configparser

runtimepath = os.getcwd()

class TestApp(wx.App):
    def OnInit(self):
        card_set = FlashCard.FlashCardSet()
        card_set.GenerateTestData()

        self.Config = configparser.ConfigParser()

        # Directories
        if not self.Config.has_section('directories'):
            self.Config.add_section('directories')
        self.Config.set('directories', 'card_dir', self.Config.get('directories', 'card_dir', fallback=runtimepath))
        self.Config.set('directories', 'image_dir', self.Config.get('directories', 'image_dir', fallback=runtimepath))
        self.Config.set('directories', 'import_dir', self.Config.get('directories', 'import_dir', fallback=runtimepath))
        self.Config.set('directories', 'export_dir', self.Config.get('directories', 'export_dir', fallback=runtimepath))

        iconfile = os.path.join(runtimepath, 'icons/pyFlashCards2-export.png')
        bitmap = wx.Bitmap(iconfile, wx.BITMAP_TYPE_PNG)

        wizard = ExportCSVWizard.ExportCSVWizard(None, -1, "Export CSV Wizard", bitmap, card_set, self.Config)
        wizard.RunWizard()

        return True

if __name__ == '__main__':
    app = TestApp()
    app.MainLoop()
