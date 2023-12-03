#-------------------------------------------------------------------------------
# Author:   Marcin Matuszkiewicz
#-------------------------------------------------------------------------------
# pyFlashCards is a multiplatform flash cards software.
# Copyright (C) 2006  Marcin Matuszkiewicz
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
#   Foundation, Inc.
#   51 Franklin Street, Fifth Floor
#   Boston
#   MA  02110-1301
#   USA.
#-------------------------------------------------------------------------------

import wx
import wx.adv
import os
import FlashCard

ID_IW_FILE_PAGE_BROWSE = wx.Window.NewControlId()

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

class FilePage(wx.adv.WizardPageSimple):
    def __init__(self, parent, dir, typepage, chapterpage):
        super(FilePage, self).__init__(parent)

        self.dir = dir
        self.typepage = typepage
        self.chapterpage = chapterpage

        sizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, 'Choose file to export')
        sizer.Add(label, 0, wx.BOTTOM, 10)

        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, 'File: ')
        self.FileTextCtrl = wx.TextCtrl(self, -1, style=wx.TE_READONLY)

        sizer1.Add(label, 0, wx.RIGHT | wx.ALIGN_CENTER, 5)
        sizer1.Add(self.FileTextCtrl, 1, wx.RIGHT | wx.ALIGN_CENTER | wx.EXPAND, 10)

        sizer.Add(sizer1, 0, wx.BOTTOM | wx.EXPAND, 10)

        button = wx.Button(self, ID_IW_FILE_PAGE_BROWSE, 'Browse')
        button.Bind(wx.EVT_BUTTON, self.OnBrowse)

        sizer.Add(button)

        self.SetSizer(sizer)
        button.SetFocus()

    def OnBrowse(self, event):
        # The previous page
        wildcard = FlashCard.GetExportWildcard(self.typepage.GetData())

        dlg = wx.FileDialog(self, message='Choose a file', defaultDir=self.dir, 
                            defaultFile='', wildcard=wildcard, style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        # Set default file name = chapter
        dlg.SetFilename(self.chapterpage.GetData())

        ans = dlg.ShowModal()
        if ans == wx.ID_OK:
            filename = dlg.GetPaths()[0]

            # Handle file extension
            root, ext = os.path.splitext(filename)
            if ext == '':
                filename = root + '.%s' % FlashCard.GetExportExt(self.typepage.GetData())

            self.dir = os.path.dirname(filename)
            self.FileTextCtrl.SetValue(filename)

        dlg.Destroy()

    def GetData(self):
        return self.FileTextCtrl.GetValue()

class ChapterPage(wx.adv.WizardPageSimple):
    def __init__(self, parent, chapters):
        super(ChapterPage, self).__init__(parent)

        sizer = wx.BoxSizer(wx.VERTICAL)
        
        label = wx.StaticText(self, -1, 'Select chapter to import into')
        f = label.GetFont()
        f.SetPointSize(12)
        label.SetFont(f)
        self.ChapterListBox = wx.ListBox(self, -1, choices=chapters)
        self.ChapterListBox.SetSelection(0)

        sizer.Add(label, 0, wx.BOTTOM, 10)
        sizer.Add(self.ChapterListBox, 0, wx.EXPAND)

        self.SetSizer(sizer)

    def GetData(self):
        return self.ChapterListBox.GetStringSelection()