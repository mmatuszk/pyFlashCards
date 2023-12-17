import wx
import FlashCard
import ImportCSVWizard
import configparser
import os

class TestApp(wx.App):
    def OnInit(self):
        self.runtimepath = os.getcwd()
        
        # Initialize the FlashCard set
        self.card_set = FlashCard.FlashCardSet()
        self.card_set.GenerateTestData()  # Assuming this method populates the FlashCardSet with test data

        # Initialize the configuration settings
        self.config = configparser.ConfigParser()

        # Assuming that these directories are defined in your config structure
        if not self.config.has_section('directories'):
            self.config.add_section('directories')
        self.config.set('directories', 'import_dir', self.config.get('directories', 'import_dir', fallback=self.runtimepath))
        self.config.set('directories', 'export_dir', self.config.get('directories', 'export_dir', fallback=self.runtimepath))

        # Run the Import CSV Wizard
        iconfile = os.path.join(self.runtimepath, 'icons/pyFlashCards2-import.png')
        bitmap = wx.Bitmap(iconfile, wx.BITMAP_TYPE_PNG)

        wizard = ImportCSVWizard.ImportCSVWizard(None, 'Import CSV Wizard', bitmap, self.card_set, self.config)
        wizard.RunWizard()
        wizard.Destroy()

        return True

if __name__ == '__main__':
    app = TestApp()
    app.MainLoop()
