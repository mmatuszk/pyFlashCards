import wx
import wx.adv
import csv
import os
import FlashCard

class FilePage(wx.adv.WizardPageSimple):
    def __init__(self, parent, dir, wildcard):
        wx.adv.WizardPageSimple.__init__(self, parent)

        self.dir = dir
        self.wildcard = wildcard

        sizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, 'Choose file to import')
        f = label.GetFont()
        f.SetPointSize(12)
        label.SetFont(f)
        sizer.Add(label, 0, wx.BOTTOM, 10)

        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, 'File: ')
        self.FileTextCtrl = wx.TextCtrl(self, -1)
        button = wx.Button(self, wx.ID_ANY, 'Browse')
        button.Bind(wx.EVT_BUTTON, self.OnBrowse)

        sizer1.Add(label, 0, wx.RIGHT, 5)
        sizer1.Add(self.FileTextCtrl, 1, wx.RIGHT, 10)
        sizer1.Add(button)

        sizer.Add(sizer1)

        self.SetSizer(sizer)

    def OnBrowse(self, event):
        p = self.GetPrev()

        dlg = wx.FileDialog(self, message='Choose a file', defaultDir=self.dir, 
                            defaultFile='', wildcard=self.wildcard, style=wx.FD_OPEN)

        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
            self.dir = os.path.dirname(filename)
            self.FileTextCtrl.SetValue(filename)

        dlg.Destroy()

    def GetData(self):
        return self.FileTextCtrl.GetValue()

class CSVMapPage(wx.adv.WizardPageSimple):
    def __init__(self, parent, file_page):
        super().__init__(parent)
        self.file_page = file_page
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        # Checkbox for indicating if the first row contains column names
        self.checkbox = wx.CheckBox(self, label="First row contains column names")
        self.checkbox.SetValue(True)
        self.sizer.Add(self.checkbox, 0, wx.ALL, 5)

        # Columns to be mapped
        self.columns = ['Front', 'Back', 'Front Image', 'Back Image', 'Chapter']
        self.column_choices = []

        # Create labels and choice dropdowns
        for col in self.columns:
            label = wx.StaticText(self, label=col + ":")
            self.sizer.Add(label, 0, wx.ALL, 2)

            choice = wx.Choice(self, choices=["Ignore"])
            self.column_choices.append(choice)
            self.sizer.Add(choice, 0, wx.EXPAND | wx.ALL, 2)

        self.SetSizer(self.sizer)
        
        # Bind the page changed event
        self.Bind(wx.adv.EVT_WIZARD_PAGE_CHANGED, self.OnPageChanged)
        
    def OnPageChanged(self, event):
        if event.GetDirection():  # True if the page is being shown, not hidden
            self.UpdateColumnChoices()
            event.Skip()  # Important to call Skip to let event processing continue

    def UpdateColumnChoices(self):
        csv_file_path = self.file_page.GetData()
        column_names = self.ReadFirstRow(csv_file_path)  # Always read the first row

        for choice in self.column_choices:
            # Update choices
            choice.Set(column_names+["Ignore"])



        # Set default selections based on the number of columns
        num_columns = len(column_names)
        
        if num_columns == 0:
            wx.MessageBox("At least 2 columns are required in the CSV file. Select a differet file", "Error", wx.OK | wx.ICON_ERROR)
            self.column_choices[0].SetSelection(0) # set front to col 0
            self.column_choices[1].SetSelection(0) # set back image to Ignore
            self.column_choices[2].SetSelection(0) # set back to col 1
            self.column_choices[3].SetSelection(0) # set back image to Ignore
            self.column_choices[4].SetSelection(0) # set chapter to Ignore
        if num_columns == 1:
            wx.MessageBox("At least 2 columns are required in the CSV file. Select a differet file", "Error", wx.OK | wx.ICON_ERROR)
            self.column_choices[0].SetSelection(1) # set front to col 0
            self.column_choices[1].SetSelection(1) # set back image to Ignore
            self.column_choices[2].SetSelection(1) # set back to col 1
            self.column_choices[3].SetSelection(1) # set back image to Ignore
            self.column_choices[4].SetSelection(1) # set chapter to Ignore                        
        elif num_columns == 2:
            self.column_choices[0].SetSelection(0) # set front to col 0
            self.column_choices[1].SetSelection(2) # set back image to Ignore
            self.column_choices[2].SetSelection(1) # set back to col 1
            self.column_choices[3].SetSelection(2) # set back image to Ignore
            self.column_choices[4].SetSelection(2) # set chapter to Ignore
        elif num_columns == 3:
            self.column_choices[0].SetSelection(0) # set front to col 0
            self.column_choices[1].SetSelection(3) # set back image to Ignore
            self.column_choices[2].SetSelection(1) # set back to col 1
            self.column_choices[3].SetSelection(3) # set back image to Ignore
            self.column_choices[4].SetSelection(2) # set chapter col 2
        elif num_columns == 4:
            self.column_choices[0].SetSelection(0) # set front to col 0
            self.column_choices[1].SetSelection(1) # set back image to col 1
            self.column_choices[2].SetSelection(2) # set back to col 2
            self.column_choices[3].SetSelection(3) # set back image col 3
            self.column_choices[4].SetSelection(4) # set chapter Ignore
        else:
            self.column_choices[0].SetSelection(0) # set front to col 0
            self.column_choices[1].SetSelection(1) # set back image to col 1
            self.column_choices[2].SetSelection(2) # set back to col 2
            self.column_choices[3].SetSelection(3) # set back image col 3
            self.column_choices[4].SetSelection(4) # set chapter to col 4
            

    def ReadFirstRow(self, csv_file_path):
        if not os.path.exists(csv_file_path):
            return []
        with open(csv_file_path, 'r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            return next(reader, [])

    def GetColumnMap(self):
        column_map = {}
        for i, choice in enumerate(self.column_choices):
            selected_index = choice.GetSelection() - 1  # Adjust for "Ignore" option
            column_map[self.columns[i].lower()] = selected_index if selected_index >= 0 else None
        return column_map

    def HasHeader(self):
        return self.checkbox.IsChecked()


class ChapterSelectionPage(wx.adv.WizardPageSimple):
    def __init__(self, parent, chapters):
        super().__init__(parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.label = wx.StaticText(self, label="Select Chapter")
        self.sizer.Add(self.label, 0, wx.EXPAND | wx.ALL, 5)

        self.chapterChoice = wx.Choice(self, choices=chapters)
        self.chapterChoice.SetSelection(0)
        self.sizer.Add(self.chapterChoice, 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(self.sizer)

    def GetChapter(self):
        return self.chapterChoice.GetStringSelection()

class ImportCSVWizard(wx.adv.Wizard):
    def __init__(self, parent, title, bitmap, card_set, config):
        super().__init__(parent, title=title, bitmap=bitmap)
        self.card_set = card_set
        self.Config = config

        self.file_page = FilePage(self, self.Config.get('directories', 'import_dir'), FlashCard.CSVWildcard)
        self.csv_map_page = CSVMapPage(self, self.file_page)
        self.chapter_selection_page = ChapterSelectionPage(self, card_set.GetChapters())

        wx.adv.WizardPageSimple.Chain(self.file_page, self.csv_map_page)
        wx.adv.WizardPageSimple.Chain(self.csv_map_page, self.chapter_selection_page)

    def RunWizard(self):
        if super().RunWizard(self.file_page):
            file_path = self.file_page.GetPath()
            column_map = self.csv_map_page.GetColumnMap()
            has_header = self.csv_map_page.HasHeader()
            chapter = self.chapter_selection_page.GetChapter()

            count = self.card_set.ImportCSV(file_path, column_map, header=has_header, create_chapter=True)
            wx.MessageBox(f"{count} cards imported", "Import Complete", wx.OK | wx.ICON_INFORMATION)
            return count


