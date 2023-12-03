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

ID_IW_FILE_PAGE_BROWSE = wx.Window.NewControlId()

class ImportTypePage(wx.adv.WizardPageSimple):
    def __init__(self, parent, types):
        wx.adv.WizardPageSimple.__init__(self, parent)

        sizer = wx.BoxSizer(wx.VERTICAL)
        
        label = wx.StaticText(self, -1, 'Choose import type')
        f = label.GetFont()
        f.SetPointSize(12)
        label.SetFont(f)
        self.ImportTypeListBox = wx.ListBox(self, -1, choices=types)
        self.ImportTypeListBox.SetSelection(0)

        sizer.Add(label, 0, wx.BOTTOM, 10)
        sizer.Add(self.ImportTypeListBox, 0, wx.EXPAND)

        self.SetSizer(sizer)

    def GetData(self):
        return self.ImportTypeListBox.GetStringSelection()

    def GetIndex(self):
        return self.ImportTypeListBox.GetSelection()

class FilePage(wx.adv.WizardPageSimple):
    def __init__(self, parent, dir, wildcards):
        wx.adv.WizardPageSimple.__init__(self, parent)

        self.dir = dir
        self.wildcards = wildcards

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
        p = self.GetPrev()
        wildcard = self.wildcards[p.GetIndex()]

        dlg = wx.FileDialog(self, message='Choose a file', defaultDir=self.dir, 
                            defaultFile='', wildcard=wildcard, style=wx.FD_OPEN)

        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
            self.dir = os.path.dirname(filename)
            self.FileTextCtrl.SetValue(filename)

        dlg.Destroy()

    def GetData(self):
        return self.FileTextCtrl.GetValue()

class ChapterPage(wx.adv.WizardPageSimple):
    def __init__(self, parent, chapters):
        wx.adv.WizardPageSimple.__init__(self, parent)

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

