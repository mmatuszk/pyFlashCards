import wx
import wx.adv
import os
import FlashCard
import ImportWizard as iw


print(os.getcwd())

class TestApp(wx.App):
    def OnInit(self):
        runtimepath = os.getcwd()
        print(runtimepath)
        self.frame = wx.Frame(None, -1, "Test Import Wizard")

        # Create a FlashCardSet instance for testing
        card_set = FlashCard.FlashCardSet()
        card_set.GenerateTestData()

        if card_set.GetChapterCount() == 0:
            wx.MessageBox("Add some chapters first", "Error", wx.OK | wx.ICON_ERROR)
            return False

        # Set the icon for the wizard
        iconfile = os.path.join(runtimepath, 'icons/pyFlashCards2-import.png')
        iconfile = os.path.normpath(iconfile)
        print(iconfile)
        bitmap = wx.Bitmap(iconfile, wx.BITMAP_TYPE_PNG)
        wizard = wx.adv.Wizard(self.frame, -1, "Import Wizard", bitmap)
        
        page1 = iw.ImportTypePage(wizard, FlashCard.ImportTypeList)
        page2 = iw.FilePage(wizard, runtimepath, FlashCard.ImportWildcard)
        page3 = iw.ChapterPage(wizard, card_set.GetChapters())
        
        wx.adv.WizardPageSimple.Chain(page1, page2)
        wx.adv.WizardPageSimple.Chain(page2, page3)

        if wizard.RunWizard(page1):
            ImportType = page1.GetData()
            ImportFile = page2.GetData()
            ImportChapter = page3.GetData()
            if os.path.exists(ImportFile):
                n = card_set.Import(ImportType, ImportFile, ImportChapter)
                wx.MessageBox(f"{n} cards imported", "Import result", wx.OK | wx.ICON_INFORMATION)

        wizard.Destroy()
        return True

if __name__ == "__main__":
    app = TestApp(redirect=False)
    app.MainLoop()
