# testExportWizard.py
import wx
import wx.adv as adv
from ExportWizard import ExportTypePage, FilePage, ChapterPage
import FlashCard
import configparser

class TestApp(wx.App):
    def OnInit(self):
       self.Config = configparser.ConfigParser()

        # Directories
        home_directory = os.path.expanduser('~')
        if not self.Config.has_section('directories'):
            self.Config.add_section('directories')
        self.Config.set('directories', 'card_dir', self.Config.get('directories', 'card_dir', fallback=home_directory))
        self.Config.set('directories', 'image_dir', self.Config.get('directories', 'image_dir', fallback=home_directory))
        self.Config.set('directories', 'import_dir', self.Config.get('directories', 'import_dir', fallback=home_directory))
        self.Config.set('directories', 'export_dir', self.Config.get('directories', 'export_dir', fallback=home_directory))

        # Create a FlashCardSet instance and populate it with test data
        card_set = FlashCard.FlashCardSet()
        card_set.GenerateTestData()

        # Extract chapter names for the ChapterPage
        chapters = card_set.GetChapters()

        # Create the wizard
        wizard = adv.Wizard(None, -1, "Export Wizard")

        # Create wizard pages
        export_type_page = ExportTypePage(wizard)
        chapter_page = ChapterPage(wizard, chapters=chapters)
        file_page = FilePage(wizard, dir=".", typepage=export_type_page, chapterpage=chapter_page)

        # Set the order of the pages
        wizard.FitToPage(export_type_page)
        adv.WizardPageSimple.Chain(export_type_page, chapter_page)
        adv.WizardPageSimple.Chain(chapter_page, file_page)

        # Show the wizard
        if wizard.RunWizard(export_type_page):
            # Process data here if wizard completed
            print("Export type:", export_type_page.GetData())
            print("Selected chapter:", chapter_page.GetData())
            print("File path:", file_page.GetData())
        else:
            print("Wizard cancelled")

        wizard.Destroy()
        return True

if __name__ == '__main__':
    app = TestApp()
    app.MainLoop()
