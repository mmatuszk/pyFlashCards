#-------------------------------------------------------------------------------
# Author:   Marcin Matuszkiewicz
# File:     ExportWizard.py
#-------------------------------------------------------------------------------

import wx
import wx.adv
import os
import FlashCard

ID_EW_FILE_PAGE_BROWSE = wx.Window.NewControlId()

class ExportTypePage(wx.adv.WizardPageSimple):
    def __init__(self, parent):
        super(ExportTypePage, self).__init__(parent)

        sizer = wx.BoxSizer(wx.VERTICAL)
        
        label = wx.StaticText(self, -1, 'Choose export type')
        f = label.GetFont()
        f.SetPointSize(12)
        label.SetFont(f)
        self.ExportTypeListBox = wx.ListBox(self, -1, choices=FlashCard.ExportTypeList)
        self.ExportTypeListBox.SetSelection(0)

        sizer.Add(label, 0, wx.BOTTOM, 10)
        sizer.Add(self.ExportTypeListBox, 0, wx.EXPAND)

        self.SetSizer(sizer)

    def GetData(self):
        return self.ExportTypeListBox.GetStringSelection()

    def GetIndex(self):
        return self.ExportTypeListBox.GetSelection()

class FileSelectionPage(wx.adv.WizardPageSimple):
    def __init__(self, parent, defaultDir, typepage, chapterpage):
        super(FileSelectionPage, self).__init__(parent)

        self.defaultDir = defaultDir
        self.typepage = typepage
        self.chapterpage = chapterpage

        sizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, 'Choose file to export')
        sizer.Add(label, 0, wx.BOTTOM, 10)

        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, 'File: ')
        self.FileTextCtrl = wx.TextCtrl(self, -1, style=wx.TE_READONLY)

        sizer1.Add(label, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)
        sizer1.Add(self.FileTextCtrl, 1, wx.EXPAND, 10)

        sizer.Add(sizer1, 0, wx.BOTTOM | wx.EXPAND, 10)

        button = wx.Button(self, ID_EW_FILE_PAGE_BROWSE, 'Browse')
        button.Bind(wx.EVT_BUTTON, self.OnBrowse)

        sizer.Add(button)

        self.SetSizer(sizer)
        button.SetFocus()

    def OnBrowse(self, event):
        wildcard = FlashCard.GetExportWildcard(self.typepage.GetData())

        dlg = wx.FileDialog(self, message='Choose a file', defaultDir=self.defaultDir, 
                            defaultFile='', wildcard=wildcard, style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

        selected_chapters = self.chapterpage.GetSelectedChapters()
        if len(selected_chapters) == 1:
            dlg.SetFilename(selected_chapters[0])
        else:
            dlg.SetFilename('')

        ans = dlg.ShowModal()
        if ans == wx.ID_OK:
            filename = dlg.GetPaths()[0]

            root, ext = os.path.splitext(filename)
            if ext == '':
                filename = root + '.%s' % FlashCard.GetExportExt(self.typepage.GetData())

            self.defaultDir = os.path.dirname(filename)
            self.FileTextCtrl.SetValue(filename)

        dlg.Destroy()

    def GetPath(self):
        return self.FileTextCtrl.GetValue()

class ChapterSelectionPage(wx.adv.WizardPageSimple):
    def __init__(self, parent, chapters):
        super().__init__(parent)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.checkList = wx.CheckListBox(self, choices=chapters)
        
        # Buttons for selecting/deselecting all chapters
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.selectAllButton = wx.Button(self, label="Select All")
        self.deselectAllButton = wx.Button(self, label="Deselect All")
        
        # Bind events to buttons
        self.selectAllButton.Bind(wx.EVT_BUTTON, self.OnSelectAll)
        self.deselectAllButton.Bind(wx.EVT_BUTTON, self.OnDeselectAll)
        
        # Add buttons to buttonSizer
        buttonSizer.Add(self.selectAllButton, 0, wx.RIGHT, 5)
        buttonSizer.Add(self.deselectAllButton, 0)
        
        # Add to main sizer
        sizer.Add(self.checkList, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(buttonSizer, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)
        self.SetSizer(sizer)

    def GetSelectedChapters(self):
        return [self.checkList.GetString(idx) for idx in self.checkList.GetCheckedItems()]

    def OnSelectAll(self, event):
        for i in range(self.checkList.GetCount()):
            self.checkList.Check(i)

    def OnDeselectAll(self, event):
        for i in range(self.checkList.GetCount()):
            self.checkList.Check(i, check=False)
    
class ExportWizard(wx.adv.Wizard):
    def __init__(self, parent, id, title, bitmap, card_set, config):
        super().__init__(parent, id, title, bitmap)
        self.card_set = card_set
        self.Config = config  # Store the configuration object

        # Create pages
        chapters = self.card_set.GetChapters()
        self.chapterPage = ChapterSelectionPage(self, chapters)
        self.exportTypePage = ExportTypePage(self)  # Assuming ExportTypePage is required
        self.filePage = FileSelectionPage(self, defaultDir=self.Config.get('directories', 'export_dir'),
                                            typepage=self.exportTypePage,
                                            chapterpage=self.chapterPage)

        # Chain pages (without DelimiterSelectionPage)
        wx.adv.WizardPageSimple.Chain(self.chapterPage, self.exportTypePage)
        wx.adv.WizardPageSimple.Chain(self.exportTypePage, self.filePage)

    def RunWizard(self):
        if super().RunWizard(self.chapterPage):
            selected_chapters = self.chapterPage.GetSelectedChapters()
            export_type = self.exportTypePage.GetData()
            filename = self.filePage.GetPath()

            # Check if the file was selected
            if filename:
                # Perform the export operation and get the number of exported cards
                num_exported_cards = self.card_set.Export(export_type, filename, selected_chapters)
                
                # Update the last used directory to config
                self.Config.set('directories', 'export_dir', os.path.dirname(filename))

                # Show a message dialog with the number of chapters and cards exported
                message = f"{len(selected_chapters)} chapters and {num_exported_cards} cards exported to {filename}."
                dlg = wx.MessageDialog(self, message, "Export Result", wx.OK | wx.ICON_INFORMATION)
                dlg.ShowModal()
                dlg.Destroy()
                return True  # Indicate successful completion
            else:
                # Show a message dialog indicating that no file was selected
                dlg = wx.MessageDialog(self, "You must select a file to export.", "Export Error", wx.OK | wx.ICON_ERROR)
                dlg.ShowModal()
                dlg.Destroy()

        # Destroy the wizard after completion
        self.Destroy()
        return False  # Indicate that the wizard did not complete successfully


