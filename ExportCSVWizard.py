#-------------------------------------------------------------------------------
# Author:   Marcin Matuszkiewicz
# File:     ExportCSVWizard.py
#-------------------------------------------------------------------------------

import wx
import wx.adv
import os
import FlashCard

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


class DelimiterSelectionPage(wx.adv.WizardPageSimple):
    def __init__(self, parent):
        super().__init__(parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, label="Select CSV delimiter:")
        # Use descriptive text for the tab character
        self.delimiterChoice = wx.Choice(self, choices=[", (Comma)", "; (Semicolon)", "Tab (\\t)", "| (Pipe)"])
        self.delimiterChoice.SetSelection(0)
        sizer.Add(label, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.delimiterChoice, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(sizer)

    def GetDelimiter(self):
        # Map the selected string back to the actual delimiter character
        delimiter_map = {
            ", (Comma)": ",",
            "; (Semicolon)": ";",
            "Tab (\\t)": "\t",
            "| (Pipe)": "|"
        }
        return delimiter_map[self.delimiterChoice.GetStringSelection()]

    
class FileSelectionPage(wx.adv.WizardPageSimple):
    def __init__(self, parent, defaultDir="."):
        super(FileSelectionPage, self).__init__(parent)

        self.defaultDir = defaultDir

        sizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, "Choose file to export")
        sizer.Add(label, 0, wx.BOTTOM, 10)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.fileTextCtrl = wx.TextCtrl(self, -1, style=wx.TE_READONLY)
        browseButton = wx.Button(self, label="Browse")
        browseButton.Bind(wx.EVT_BUTTON, self.OnBrowse)

        hsizer.Add(self.fileTextCtrl, 1, wx.EXPAND | wx.RIGHT, 5)
        hsizer.Add(browseButton, 0, wx.EXPAND)

        sizer.Add(hsizer, 0, wx.EXPAND | wx.BOTTOM, 10)
        self.SetSizer(sizer)

    def OnBrowse(self, event):
        dlg = wx.FileDialog(self, "Save CSV file", defaultDir=self.defaultDir, 
                            defaultFile="", wildcard="CSV files (*.csv)|*.csv",
                            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
            self.fileTextCtrl.SetValue(filename)

        dlg.Destroy()

    def GetPath(self):
        return self.fileTextCtrl.GetValue()

class ExportCSVWizard(wx.adv.Wizard):
    def __init__(self, parent, id, title, bitmap, card_set, config):
        super().__init__(parent, id, title, bitmap)
        self.card_set = card_set
        self.Config = config  # Store the configuration object

        # Create pages
        chapters = self.card_set.GetChapters()
        self.chapterPage = ChapterSelectionPage(self, chapters)
        self.delimiterPage = DelimiterSelectionPage(self)
        self.filePage = FileSelectionPage(self, defaultDir=self.Config.get('directories', 'export_dir'))

        # Chain pages
        wx.adv.WizardPageSimple.Chain(self.chapterPage, self.delimiterPage)
        wx.adv.WizardPageSimple.Chain(self.delimiterPage, self.filePage)

    def RunWizard(self):
        if super().RunWizard(self.chapterPage):
            selected_chapters = self.chapterPage.GetSelectedChapters()
            delimiter = self.delimiterPage.GetDelimiter()
            filename = self.filePage.GetPath()

            # Check if the file was selected
            if filename:
                # Perform the export operation and get the number of exported cards
                num_exported_cards = self.card_set.ExportCSV(filename, selected_chapters, delimiter)
                
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
        return False  # Indicate that the wizard did not complete successfully

        # Destroy the wizard after completion
        self.Destroy()
