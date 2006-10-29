import wx
import wx.wizard as wiz
import os

ID_IW_FILE_PAGE_BROWSE = wx.NewId()

class ImportTypePage(wiz.WizardPageSimple):
    def __init__(self, parent, types):
        wiz.WizardPageSimple.__init__(self, parent)

        sizer = wx.BoxSizer(wx.VERTICAL)
        
        label = wx.StaticText(self, -1, 'Choose import type')
        f = label.GetFont()
        f.SetPointSize(12)
        label.SetFont(f)
        self.ImportTypeListBox = wx.ListBox(self, -1, choices = types)
        self.ImportTypeListBox.SetSelection(0)

        sizer.Add(label, 0, wx.BOTTOM, 10)
        sizer.Add(self.ImportTypeListBox, 0, wx.EXPAND)

        self.SetSizer(sizer)

    def GetData(self):
        return self.ImportTypeListBox.GetStringSelection()

class FilePage(wiz.WizardPageSimple):
    def __init__(self, parent, dir):
        wiz.WizardPageSimple.__init__(self, parent)

        self.dir = dir

        sizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, 'Choose file to import')
        f = label.GetFont()
        f.SetPointSize(12)
        label.SetFont(f)
        sizer.Add(label, 0, wx.BOTTOM, 10)

        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, 'File: ')
        self.FileTextCtrl = wx.TextCtrl(self, -1)
        button = wx.Button(self, ID_IW_FILE_PAGE_BROWSE, 'Browse')
        button.Bind(wx.EVT_BUTTON, self.OnBrowse)

        sizer1.Add(label, 0, wx.RIGHT, 5)
        sizer1.Add(self.FileTextCtrl, 1, wx.RIGHT, 10)
        sizer1.Add(button)

        sizer.Add(sizer1)

        self.SetSizer(sizer)

    def OnBrowse(self, event):
        dlg = wx.FileDialog(self, message='Choose a file', defaultDir = self.dir, 
                    defaultFile='', style=wx.OPEN)

        ans = dlg.ShowModal()
        if ans == wx.ID_OK:
            filename = dlg.GetPaths()[0]
            self.dir = os.path.dirname(filename)
            self.FileTextCtrl.SetValue(filename)

        dlg.Destroy()

    def GetData(self):
        return self.FileTextCtrl.GetValue()

class ChapterPage(wiz.WizardPageSimple):
    def __init__(self, parent, chapters):
        wiz.WizardPageSimple.__init__(self, parent)

        sizer = wx.BoxSizer(wx.VERTICAL)
        
        label = wx.StaticText(self, -1, 'Select chapter to import into')
        f = label.GetFont()
        f.SetPointSize(12)
        label.SetFont(f)
        self.ChapterListBox = wx.ListBox(self, -1, choices = chapters)
        self.ChapterListBox.SetSelection(0)

        sizer.Add(label, 0, wx.BOTTOM, 10)
        sizer.Add(self.ChapterListBox, 0, wx.EXPAND)

        self.SetSizer(sizer)

    def GetData(self):
        return self.ChapterListBox.GetStringSelection()

