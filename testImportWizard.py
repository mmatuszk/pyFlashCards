# testImportWizard.py
import wx
import wx.adv as adv
import ImportWizard  # Changed from ExportWizard to ImportWizard
import FlashCard
import os
import configparser

runtimepath = os.getcwd()

class TestApp(wx.App):
    def OnInit(self):
        self.CardSet = FlashCard.FlashCardSet()
        self.CardSet.GenerateTestData()

        self.Config = configparser.ConfigParser()
        self.runtimepath = runtimepath

        # Directories
        if not self.Config.has_section('directories'):
            self.Config.add_section('directories')
        self.Config.set('directories', 'card_dir', self.Config.get('directories', 'card_dir', fallback=runtimepath))
        self.Config.set('directories', 'image_dir', self.Config.get('directories', 'image_dir', fallback=runtimepath))
        self.Config.set('directories', 'import_dir', self.Config.get('directories', 'import_dir', fallback=runtimepath))
        self.Config.set('directories', 'export_dir', self.Config.get('directories', 'export_dir', fallback=runtimepath))

        iconfile = os.path.join(self.runtimepath, 'icons/pyFlashCards2-import.png')

        bitmap = wx.Bitmap(iconfile, wx.BITMAP_TYPE_PNG)

        wizard = ImportWizard.ImportWizard(None, -1, "Import Wizard", bitmap, self.CardSet, self.Config)
        wizard.RunWizard()

        wizard.Destroy()

        return True

if __name__ == '__main__':
    app = TestApp()
    app.MainLoop()
