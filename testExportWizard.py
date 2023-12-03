# testExportWizard.py
import wx
import wx.adv as adv
from ExportWizard import ExportTypePage, FilePage, ChapterPage
import FlashCard

class TestApp(wx.App):
    def OnInit(self):
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
