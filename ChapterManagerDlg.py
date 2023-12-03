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
import FlashCard

def create(parent):
    return ChapterManagerDlg(parent)

ID_CHAPTERMANAGERDLG                    = wx.Window.NewControlId()
ID_CHAPTERMANAGERDLGCHAPTERLISTCTRL     = wx.Window.NewControlId()
ID_CHAPTERMANAGERDLGCHAPTERTITLEENTRY   = wx.Window.NewControlId()
ID_CHAPTERMANAGERDLGMOVEUPBUTTON        = wx.Window.NewControlId()
ID_CHAPTERMANAGERDLGMOVEDOWNBUTTON      = wx.Window.NewControlId()
ID_CHAPTERMANAGERDLGDELETEBUTTON        = wx.Window.NewControlId()


class ChapterManagerDlg(wx.Dialog):
    def _init_ctrls(self, prnt):
        wx.Dialog.__init__(self, id=ID_CHAPTERMANAGERDLG,
              name=u'ChapterManagerDlg', parent=prnt, pos=wx.Point(630, 421),
              size=wx.Size(364, 345),
              style=wx.RESIZE_BORDER | wx.DEFAULT_DIALOG_STYLE,
              title=u'Chapter Manager')
        self.SetClientSize(wx.Size(365, 345))

        # Create controls
        self.ChapterListCtrl = wx.ListCtrl(self, ID_CHAPTERMANAGERDLGCHAPTERLISTCTRL,
                size=(330, 270), style = wx.LC_REPORT)

        self.MoveUpButton   = wx.Button(self, ID_CHAPTERMANAGERDLGMOVEUPBUTTON, 'Up')
        self.MoveDownButton = wx.Button(self, ID_CHAPTERMANAGERDLGMOVEDOWNBUTTON, 'Down')
        self.DeleteButton   = wx.Button(self, ID_CHAPTERMANAGERDLGDELETEBUTTON, 'Delete')

        self.ChapterTitleEntry = wx.TextCtrl(self, ID_CHAPTERMANAGERDLGCHAPTERTITLEENTRY,
              style=wx.TE_PROCESS_ENTER, value=u'')
        self.ChapterTitleLabel = wx.StaticText(self, label = 'Chapter title')

        # Bind messages
        self.ChapterListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED,
              self.OnChapterListCtrlListItemSelected,
              id=ID_CHAPTERMANAGERDLGCHAPTERLISTCTRL)
        self.ChapterListCtrl.Bind(wx.EVT_LIST_ITEM_DESELECTED,
              self.OnChapterListCtrlListItemDeselected,
              id=ID_CHAPTERMANAGERDLGCHAPTERLISTCTRL)
        self.ChapterListCtrl.Bind(wx.EVT_CHAR, self.OnChapterListCtrlChar)

        self.ChapterTitleEntry.Bind(wx.EVT_TEXT_ENTER,
              self.OnChapterTitleEntryTextEnter,
              id=ID_CHAPTERMANAGERDLGCHAPTERTITLEENTRY)
        self.ChapterTitleEntry.Bind(wx.EVT_CHAR, self.OnChapterTitleEntryChar)
        self.MoveUpButton.Bind(wx.EVT_BUTTON, self.OnMoveUpButton)
        self.MoveDownButton.Bind(wx.EVT_BUTTON, self.OnMoveDownButton)
        self.DeleteButton.Bind(wx.EVT_BUTTON, self.OnDeleteButton)

        # Create a layout 
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.ChapterListCtrl, 1, wx.EXPAND | wx.ALL, 5)

        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(self.MoveUpButton, 0, wx.ALL, 5)
        vsizer.Add(self.MoveDownButton, 0, wx.ALL, 5)
        vsizer.Add(self.DeleteButton, 0, wx.ALL, 5)

        hsizer.Add(vsizer, 0, wx.ALIGN_CENTER_VERTICAL)

        main_sizer.Add(hsizer, 1, wx.EXPAND)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.ChapterTitleLabel, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        hsizer.Add(self.ChapterTitleEntry, 1, wx.EXPAND | wx.ALL, 15) 
        main_sizer.Add(hsizer, 0, wx.EXPAND)

        self.SetSizer(main_sizer)
        self.Fit()


    def __init__(self, parent, CardSet):
        self._init_ctrls(parent)

        self.CardSet = CardSet
        self.ChapterEditIndex = -1
        self.OldChapterTitle = ''

        width = self.ChapterListCtrl.GetSize()[0]-4
        self.ChapterListCtrl.InsertColumn(0, "Chapter", width = width*0.35)
        self.ChapterListCtrl.InsertColumn(1, "Title", width = width*0.6)

        self.AddChapters2List(self.CardSet.GetChapters())

        self.ChapterTitleEntry.SetFocus()

    def AddChapters2List(self, list):
        for chapter in list:
            label = self.CardSet.GetChapterLabel(chapter)
            # Insert cards at the end of the list by getting the index from the
            # number of items in the list
            index = self.ChapterListCtrl.InsertItem(self.ChapterListCtrl.GetItemCount(), label)
            self.ChapterListCtrl.SetItem(index, 1, chapter)


    def GetCardSet(self):
        return self.CardSet

    def OnChapterTitleEntryTextEnter(self, event):
        chapter = self.ChapterTitleEntry.GetValue()
        chapter = chapter.lstrip().rstrip()

        if chapter == '':
            MsgWin = wx.MessageDialog(self, 'Enter a valid chapter title', 'Error', wx.OK | wx.ICON_ERROR)
            MsgWin.CenterOnParent()
            MsgWin.ShowModal()
            return

        if self.ChapterEditIndex < 0:
            try:
                self.CardSet.AddChapter(chapter)
                self.AddChapters2List([chapter])
                self.ChapterTitleEntry.SetValue('')
            except FlashCard.FlashCardError as err:  # Updated to Python 3 syntax
                MsgWin = wx.MessageDialog(self, str(err), 'Error', wx.OK | wx.ICON_ERROR)
                MsgWin.ShowModal()
        else:
            if self.OldChapterTitle == chapter:
                return

            self.ChapterListCtrl.SetStringItem(self.ChapterEditIndex, 1, chapter)
            self.ChapterListCtrl.SetItemState(self.ChapterEditIndex, 0, wx.LIST_STATE_SELECTED)
            self.ChapterTitleEntry.SetValue('')

            self.CardSet.RenameChapter(self.OldChapterTitle, chapter)

            self.ChapterEditIndex = -1

    def OnChapterListCtrlListItemSelected(self, event):
        index = event.GetIndex()
        if self.ChapterListCtrl.GetSelectedItemCount() == 1:
            title = self.ChapterListCtrl.GetItem(index, 1).GetText()
            self.OldChapterTitle = title
            self.ChapterTitleEntry.SetValue(title)
            self.ChapterEditIndex = index
        else:
            self.ChapterTitleEntry.SetValue('')
            self.ChapterEditIndex = -1

    def OnChapterListCtrlListItemDeselected(self, event):
        if self.ChapterListCtrl.GetSelectedItemCount() == 0:
            self.ChapterTitleEntry.SetValue('')
            self.ChapterEditIndex = -1

    def OnChapterListCtrlChar(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_DELETE or keycode == wx.WXK_BACK:
            self.DeleteSelectedChapters()
        elif keycode == wx.WXK_ESCAPE:
            index = self.ChapterListCtrl.GetFirstSelected()
            
            while index != -1:
                self.ChapterListCtrl.SetItemState(index, 0, wx.LIST_STATE_SELECTED)
                index = self.ChapterListCtrl.GetNextSelected(index)
            self.ChapterTitleEntry.SetValue('')
            self.ChapterEditIndex = -1
        else:
            event.Skip()

    def OnChapterTitleEntryChar(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_ESCAPE:
            if self.ChapterEditIndex > 0:
                self.ChapterListCtrl.SetItemState(self.ChapterEditIndex, 0, wx.LIST_STATE_SELECTED)
                self.ChapterTitleEntry.SetValue('')

                self.ChapterEditIndex = -1
        else:
            event.Skip()

    def OnMoveUpButton(self, event):
        self.MoveSelectedChaptersUp()

    def OnMoveDownButton(self, event):
        self.MoveSelectedChaptersDown()

    def OnDeleteButton(self, event):
        self.DeleteSelectedChapters()

    def DeleteSelectedChapters(self):
        index = self.ChapterListCtrl.GetFirstSelected()
        
        while index != -1:
            item = self.ChapterListCtrl.GetItem(index, 1)
            chapter = item.GetText()
            self.CardSet.RemoveChapter(chapter)
            self.ChapterListCtrl.DeleteItem(index)
            index = self.ChapterListCtrl.GetNextSelected(index-1)

        self.ChapterListCtrl.DeleteAllItems()
        self.AddChapters2List(self.CardSet.GetChapters())
        self.ChapterEditIndex = -1
        self.ChapterTitleEntry.SetValue('')

    def MoveSelectedChaptersUp(self):
        # get info about selected card
        first = self.ChapterListCtrl.GetFirstSelected()
        # if no cards are selected or we are already at the top of the list, exit 
        if first < 1:
            return

        list = [first]

        i = first
        while i != -1:
            i = self.ChapterListCtrl.GetNextSelected(i)
            if i > 0:
                list.append(i)

        # move cards around in the card set
        self.CardSet.MoveChaptersUp(list)

        # update the state of the card list control
        self.ChapterListCtrl.DeleteAllItems()
        self.AddChapters2List(self.CardSet.GetChapters())
        for i in list:
            self.ChapterListCtrl.SetItemState(i-1, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)

    def MoveSelectedChaptersDown(self):
        # get info about selected card
        first = self.ChapterListCtrl.GetFirstSelected()
        # if no cards are selected or we are already at the top of the list, exit 
        if first == -1:
            return

        list = [first]

        i = first
        while i != -1:
            i = self.ChapterListCtrl.GetNextSelected(i)
            if i > 0:
                list.append(i)

        list.reverse()

        if list[0] == self.ChapterListCtrl.GetItemCount() - 1:
            # if the last item is selected there is nothing to do
            return

        # move cards around in the card set
        self.CardSet.MoveChaptersDown(list)

        # update the state of the card list control
        self.ChapterListCtrl.DeleteAllItems()
        self.AddChapters2List(self.CardSet.GetChapters())
        for i in list:
            self.ChapterListCtrl.SetItemState(i+1, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
