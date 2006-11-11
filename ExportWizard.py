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
# CVS information
# $Source: /cvsroot/pyflashcards/pyFlashCards/ExportWizard.py,v $
# $Revision: 1.1 $
# $Date: 2006/11/11 00:46:58 $
# $Author: marcin $
#-------------------------------------------------------------------------------
import wx
import wx.wizard as wiz
import os

import FlashCard

ID_IW_FILE_PAGE_BROWSE = wx.NewId()

class ExportTypePage(wiz.WizardPageSimple):
    def __init__(self, parent):
        wiz.WizardPageSimple.__init__(self, parent)

        sizer = wx.BoxSizer(wx.VERTICAL)
        
        label = wx.StaticText(self, -1, 'Choose export type')
        f = label.GetFont()
        f.SetPointSize(12)
        label.SetFont(f)
        self.ExportTypeListBox = wx.ListBox(self, -1, choices = FlashCard.ExportTypeList)
        self.ExportTypeListBox.SetSelection(0)

        sizer.Add(label, 0, wx.BOTTOM, 10)
        sizer.Add(self.ExportTypeListBox, 0, wx.EXPAND)

        self.SetSizer(sizer)

    def GetData(self):
        return self.ExportTypeListBox.GetStringSelection()

    def GetIndex(self):
        return self.ExportTypeListBox.GetSelection()

class FilePage(wiz.WizardPageSimple):
    def __init__(self, parent, dir):
        wiz.WizardPageSimple.__init__(self, parent)

        self.dir = dir

        sizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, 'Choose file to export')
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
        # The previous page
        p = self.GetPrev()
        wildcard = FlashCard.GetExportWildcard(p.GetData())

        dlg = wx.FileDialog(self, message='Choose a file', defaultDir = self.dir, 
                    defaultFile='', wildcard=wildcard, style=wx.SAVE | wx.OVERWRITE_PROMPT)

        ans = dlg.ShowModal()
        if ans == wx.ID_OK:
            filename = dlg.GetPaths()[0]

            # On Linux we need to make sure that the extension is added
            # On windows the dialog adds the extension automatically
            root, ext = os.path.splitext(filename)
            if ext == '':
                filename = root+'.%s' % FlashCard.GetExportExt(p.GetData())

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

