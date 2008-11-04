#-------------------------------------------------------------------------------
# AutoCorrDlg.py
# Dialog for editing find replace pairs
#
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
# $Source: /cvsroot/pyflashcards/pyFlashCards/AutoCorrDlg.py,v $
# $Revision: 1.7 $
# $Date: 2008/11/04 05:08:55 $
# $Author: marcin201 $
#-------------------------------------------------------------------------------

import wx

ID_AUTOCORRDLG_ON_NEW_REPLACE       = wx.NewId()
ID_AUTOCORRDLG_ON_DELETE            = wx.NewId()

class AutoCorrDlg(wx.Dialog):
    def __init__(
            self, parent, ID, autocorr, title='AutoCorr', 
            size=(500, 500), pos=wx.DefaultPosition, 
            style=wx.DEFAULT_DIALOG_STYLE):
        # Instead of calling wx.Dialog.__init__ we precreate the dialog
        # so we can set an extra style that must be set before
        # creation, and then we create the GUI dialog using the Create
        # method.
        #pre = wx.PreDialog()
        #pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        #pre.Create(parent, ID, title, pos, size, style)

        # This next step is the most important, it turns this Python
        # object into the real wrapper of the dialog (instead of pre)
        # as far as the wxPython extension is concerned.
        #self.PostCreate(pre)
        wx.Dialog.__init__(self, id=ID, name=u'AutoCorrDlg',
              parent=parent, size=size, style=style, title=title)

        # Now continue with the normal construction of the dialog
        # contents
        self.init_ctrls(parent)

        # Bind methods
        self.Bind(wx.EVT_BUTTON, self.OnNewReplace, self.NewReplaceButton)
        self.Bind(wx.EVT_BUTTON, self.OnDelete, self.DeleteButton)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.ReplaceWithListCtrl)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected, self.ReplaceWithListCtrl)
        self.Bind(wx.EVT_CHAR, self.ReplaceTextCtrlEvtChar, self.ReplaceTextCtrl)
        self.Bind(wx.EVT_TEXT, self.ReplaceTextCtrlEvtText, self.ReplaceTextCtrl)
        self.Bind(wx.EVT_CHECKBOX, self.OnEnableCheckBox, self.EnableCheckBox)

        self.autocorr = autocorr

        self.InitFindReplaceUI()


    def init_ctrls(self, parent):
        self.ReplaceLabel = wx.StaticText(self, -1, 'Replace')
        self.WithLabel = wx.StaticText(self, -1, 'With')
        self.ReplaceTextCtrl = wx.TextCtrl(self, -1)
        self.WithTextCtrl = wx.TextCtrl(self, -1)
        self.NewReplaceButton = wx.Button(self, ID_AUTOCORRDLG_ON_NEW_REPLACE, 'New')
        self.ReplaceWithListCtrl = wx.ListCtrl(self, -1, size=(100, 350), style=
                wx.LC_REPORT | 
                wx.LC_NO_HEADER |
                wx.LC_SINGLE_SEL)
        self.DeleteButton = wx.Button(self, ID_AUTOCORRDLG_ON_DELETE, 'Delete')
        self.EnableCheckBox = wx.CheckBox(self, -1, 'Enable Autocorrect')

        # Disable buttons
        self.NewReplaceButton.Disable()
        self.DeleteButton.Disable()

        # resize of the windows
        size = self.WithTextCtrl.GetSize()
        size[0] *= 2.5
        self.WithTextCtrl.SetInitialSize(size)

        gbs = wx.GridBagSizer(5,3)

        row = 0
        gbs.Add(self.ReplaceLabel, (row,0), wx.DefaultSpan, wx.TOP | wx.LEFT, 10)
        gbs.Add(self.WithLabel, (row,1), wx.DefaultSpan, wx.TOP | wx.LEFT, 10)
        row += 1
        gbs.Add(self.ReplaceTextCtrl, (row, 0), wx.DefaultSpan, wx.TOP | wx.LEFT, 10)
        gbs.Add(self.WithTextCtrl, (row, 1), wx.DefaultSpan, wx.TOP | wx.LEFT, 10)
        gbs.Add(self.NewReplaceButton, (row, 2), wx.DefaultSpan, wx.TOP | wx.LEFT | wx.RIGHT | wx.ALIGN_CENTER, 10)
        row += 1
        gbs.Add(self.ReplaceWithListCtrl, (row,0), (1,2), wx.TOP | wx.LEFT | wx.EXPAND, 10)
        gbs.Add(self.DeleteButton, (row, 2), wx.DefaultSpan, wx.TOP | wx.LEFT | wx. RIGHT | wx.ALIGN_CENTER, 10)
        row += 1
        gbs.Add(self.EnableCheckBox, (row, 0), (1,2), wx.TOP | wx.LEFT, 10)
        row += 1

        self.OkButton = wx.Button(self, wx.ID_OK)
        self.OkButton.SetDefault()

        btnsizer = wx.StdDialogButtonSizer()

        btnsizer.Add(self.OkButton)
        btnsizer.Realize()

        gbs.Add(btnsizer, (row, 0), (1, 3), wx.ALIGN_RIGHT | wx.ALL, 10)

        self.SetSizer(gbs)
        self.Fit()

    def InitFindReplaceUI(self):
        findWidth = self.ReplaceTextCtrl.GetSize()[0]+10

        self.ReplaceWithListCtrl.InsertColumn(0, "Replace", width = findWidth)
        self.ReplaceWithListCtrl.InsertColumn(1, "With")

        for replaceStr, withStr in self.autocorr.GetItems():
            # Insert cards at the end of the list by getting the index from the
            # number of items in the list
            index = self.ReplaceWithListCtrl.GetItemCount()
            self.ReplaceWithListCtrl.InsertStringItem(index, replaceStr)
            self.ReplaceWithListCtrl.SetStringItem(index, 1, withStr)

        self.EnableCheckBox.SetValue(self.autocorr.GetSetEnable())

    def GetData(self):
        return self.autocorr

    def OnNewReplace(self, event):
        replaceStr =  self.ReplaceTextCtrl.GetValue()
        withStr = self.WithTextCtrl.GetValue()

        index = self.ReplaceWithListCtrl.GetFirstSelected()
        if index < 0:
            index = self.autocorr.InsertItem(replaceStr, withStr)

            # update the GUI
            self.ReplaceWithListCtrl.InsertStringItem(index, replaceStr)            
            self.ReplaceWithListCtrl.SetStringItem(index, 1, withStr)
            self.ReplaceTextCtrl.SetValue('')
            self.WithTextCtrl.SetValue('')
            self.ReplaceTextCtrl.SetFocus()
        else:
            self.autocorr.ReplaceItem(index, replaceStr, withStr)

            # update the GUI
            self.ReplaceWithListCtrl.SetStringItem(index, 0,replaceStr)            
            self.ReplaceWithListCtrl.SetStringItem(index, 1, withStr)
            self.ReplaceTextCtrl.SetValue('')
            self.WithTextCtrl.SetValue('')
            self.ReplaceTextCtrl.SetFocus()

            # deselected updated item
            self.ReplaceWithListCtrl.SetItemState(index, 0, wx.LIST_STATE_SELECTED)

    def OnDelete(self, event):
        index = self.ReplaceWithListCtrl.GetFirstSelected()

        if index < 0:
            return

        self.ReplaceWithListCtrl.SetItemState(index, 0, wx.LIST_STATE_SELECTED)
        self.ReplaceWithListCtrl.DeleteItem(index)

        self.autocorr.DeleteItem(index)

        self.ReplaceTextCtrl.SetValue('')
        self.WithTextCtrl.SetValue('')
        self.ReplaceTextCtrl.SetFocus()

        self.NewReplaceButton.SetLabel('New')

    def OnItemSelected(self, event):
        event.Skip()

        index = self.ReplaceWithListCtrl.GetFirstSelected()
        replaceStr, withStr = self.autocorr.GetItem(index)
        self.ReplaceTextCtrl.SetValue(replaceStr)
        self.WithTextCtrl.SetValue(withStr)
        self.NewReplaceButton.SetLabel('Replace')

        self.DeleteButton.Enable()

    def OnItemDeselected(self, event):
        event.Skip()

        self.DeleteButton.Disable()

    def ReplaceTextCtrlEvtChar(self, event):
        charCode = event.GetCharCode()
        event.Skip()

        if self.ReplaceWithListCtrl.GetSelectedItemCount() == 0:
            return

    def ReplaceTextCtrlEvtText(self, event):
        event.Skip()

        if len(event.GetString()) > 0:
            self.NewReplaceButton.Enable()
        else:
            self.NewReplaceButton.Disable()

        if self.ReplaceWithListCtrl.GetSelectedItemCount() == 0:
            # If no item is selected, but the text in RepalceTextCtrl is already in autocorr
            # we need to select the item and change button label to replace
            i = self.autocorr.FindReplaceStr(event.GetString())
            if i >= 0:
                self.ReplaceWithListCtrl.SetItemState(i, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
        else:
            index = self.ReplaceWithListCtrl.GetFirstSelected()
            replaceStr, withStr = self.autocorr.GetItem(index)

            if replaceStr == event.GetString():
                return

            self.NewReplaceButton.SetLabel('New')
            # Deselect item in the list control
            self.ReplaceWithListCtrl.SetItemState(index, 0, wx.LIST_STATE_SELECTED)

    def OnEnableCheckBox(self, event):
        if event.IsChecked():
            self.autocorr.Enable()
        else:
            self.autocorr.Disable()

        event.Skip()
