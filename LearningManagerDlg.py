#Boa:Dialog:LearningManagerDlg
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
# $Source: /cvsroot/pyflashcards/pyFlashCards/LearningManagerDlg.py,v $
# $Revision: 1.4 $
# $Date: 2008/10/04 21:29:51 $
# $Author: marcin $
#-------------------------------------------------------------------------------

import wx

def create(parent):
    return LearningManagerDlg(parent)

[wxID_LEARNINGMANAGERDLG, wxID_LEARNINGMANAGERDLGADDBUTTON, 
 wxID_LEARNINGMANAGERDLGAVAILABLECHAPTERSLISTCTRL, 
 wxID_LEARNINGMANAGERDLGREMOVEBUTTON, 
 wxID_LEARNINGMANAGERDLGSELECTEDCHAPTERSLISTCTRL, 
 wxID_LEARNINGMANAGERDLGSTATICTEXT1, wxID_LEARNINGMANAGERDLGSTATICTEXT2, 
 wxID_LEARNINGMANAGERDLGSTATICTEXT3, wxID_LEARNINGMANAGERDLGTESTCARDSCOUNT, 
] = [wx.NewId() for _init_ctrls in range(9)]

class LearningManagerDlg(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_LEARNINGMANAGERDLG,
              name=u'LearningManagerDlg', parent=prnt, pos=wx.Point(489, 250),
              size=wx.Size(592, 471), style=wx.DEFAULT_DIALOG_STYLE,
              title=u'Learning Manger Dialog')
        self.SetClientSize(wx.Size(584, 433))

        self.staticText1 = wx.StaticText(id=wxID_LEARNINGMANAGERDLGSTATICTEXT1,
              label=u'Available chapters', name='staticText1', parent=self,
              pos=wx.Point(16, 16), size=wx.Size(87, 13), style=0)

        self.staticText2 = wx.StaticText(id=wxID_LEARNINGMANAGERDLGSTATICTEXT2,
              label=u'Selected chapters', name='staticText2', parent=self,
              pos=wx.Point(336, 16), size=wx.Size(86, 13), style=0)

        self.AddButton = wx.BitmapButton(bitmap=wx.Bitmap(u'icons/right_arrow.png',
              wx.BITMAP_TYPE_PNG), id=wxID_LEARNINGMANAGERDLGADDBUTTON,
              name=u'AddButton', parent=self, pos=wx.Point(272, 144),
              size=wx.Size(34, 34), style=wx.BU_AUTODRAW)
        self.AddButton.Bind(wx.EVT_BUTTON, self.OnAddButtonButton,
              id=wxID_LEARNINGMANAGERDLGADDBUTTON)

        self.RemoveButton = wx.BitmapButton(bitmap=wx.Bitmap(u'icons/left_arrow.png',
              wx.BITMAP_TYPE_PNG), id=wxID_LEARNINGMANAGERDLGREMOVEBUTTON,
              name=u'RemoveButton', parent=self, pos=wx.Point(272, 192),
              size=wx.Size(34, 34), style=wx.BU_AUTODRAW)
        self.RemoveButton.Bind(wx.EVT_BUTTON, self.OnRemoveButtonButton,
              id=wxID_LEARNINGMANAGERDLGREMOVEBUTTON)

        self.AvailableChaptersListCtrl = wx.ListCtrl(id=wxID_LEARNINGMANAGERDLGAVAILABLECHAPTERSLISTCTRL,
              name=u'AvailableChaptersListCtrl', parent=self, pos=wx.Point(16,
              40), size=wx.Size(230, 350), style=wx.LC_REPORT)

        self.SelectedChaptersListCtrl = wx.ListCtrl(id=wxID_LEARNINGMANAGERDLGSELECTEDCHAPTERSLISTCTRL,
              name=u'SelectedChaptersListCtrl', parent=self, pos=wx.Point(336,
              40), size=wx.Size(230, 350), style=wx.LC_REPORT)

        self.staticText3 = wx.StaticText(id=wxID_LEARNINGMANAGERDLGSTATICTEXT3,
              label=u'Selected cards', name='staticText3', parent=self,
              pos=wx.Point(336, 400), size=wx.Size(71, 13), style=0)

        self.TestCardsCount = wx.TextCtrl(id=wxID_LEARNINGMANAGERDLGTESTCARDSCOUNT,
              name=u'TestCardsCount', parent=self, pos=wx.Point(424, 396),
              size=wx.Size(48, 21), style=wx.TE_READONLY, value=u'')

    def __init__(self, parent, CardSet):
        self._init_ctrls(parent)

        self.CardSet = CardSet

        # Add columns to the chapters list controls
        ListWidth = self.AvailableChaptersListCtrl.GetSize()[0]

        self.AvailableChaptersListCtrl.InsertColumn(0, 'Chapter',
                                                    width=ListWidth*0.8-2)
        self.AvailableChaptersListCtrl.InsertColumn(1, 'Cards',
                                                    width=ListWidth*0.2-2)
        ListWidth = self.SelectedChaptersListCtrl.GetSize()[0]

        self.SelectedChaptersListCtrl.InsertColumn(0, 'Chapter',
                                                    width=ListWidth*0.8-2)
        self.SelectedChaptersListCtrl.InsertColumn(1, 'Cards',
                                                    width=ListWidth*0.2-2)

        # Populate available chapaters list control
        for chapter in self.CardSet.GetAvailableChapters():
            count = self.CardSet.GetChapterCardCount(chapter)
            # Insert cards at the end of the list by getting the index from the
            # number of items in the list
            index = self.AvailableChaptersListCtrl.GetItemCount()
            self.AvailableChaptersListCtrl.InsertStringItem(index, chapter)
            self.AvailableChaptersListCtrl.SetStringItem(index, 1, `count`)

        # Populate available chapaters list control
        for chapter in self.CardSet.GetSelectedChapters():
            count = self.CardSet.GetChapterCardCount(chapter)
            # Insert cards at the end of the list by getting the index from the
            # number of items in the list
            index = self.SelectedChaptersListCtrl.GetItemCount()
            self.SelectedChaptersListCtrl.InsertStringItem(index, chapter)
            self.SelectedChaptersListCtrl.SetStringItem(index, 1, `count`)

        # Set test cards count
        self.TestCardsCount.SetValue(`self.CardSet.GetTestCardsCount()`)


    def GetCardSet(self):
        return self.CardSet

    def OnAddButtonButton(self, event):
        index = self.AvailableChaptersListCtrl.GetFirstSelected()

        while index != -1:
            # Save chapter information
            chapter = self.CardSet.GetAvailableChapters()[index]

            # Remove the chapter from ListCtrl
            self.AvailableChaptersListCtrl.DeleteItem(index)

            # Move the chapter from availalbe list to selected list and add the
            # chapter chards to the learning set
            self.CardSet.SelectChapter(index)

            # Add the chapter to the selected chapters ListCtrl
            count = self.CardSet.GetChapterCardCount(chapter)
            i = self.SelectedChaptersListCtrl.GetItemCount()
            self.SelectedChaptersListCtrl.InsertStringItem(i, chapter)
            self.SelectedChaptersListCtrl.SetStringItem(i, 1, `count`)

            # Next selected item
            index = self.AvailableChaptersListCtrl.GetNextSelected(index-1)


        self.TestCardsCount.SetValue(`self.CardSet.GetTestCardsCount()`)

    def OnRemoveButtonButton(self, event):
        print "Removing chapter"
        index = self.SelectedChaptersListCtrl.GetFirstSelected()

        while index != -1:
            # Save chapter information
            chapter = self.CardSet.GetSelectedChapters()[index]

            # Remove the chapter from ListCtrl
            self.SelectedChaptersListCtrl.DeleteItem(index)

            # Move the chapter from availalbe list to selected list and add the
            # chapter chards to the learning set
            insert = self.CardSet.DeselectChapter(index)

            # Add the chapter to the selected chapters ListCtrl
            count = self.CardSet.GetChapterCardCount(chapter)
            print 'Count: ' + `count`
            print 'Insert: ' + `insert`
            self.AvailableChaptersListCtrl.InsertStringItem(insert, chapter)
            self.AvailableChaptersListCtrl.SetStringItem(insert, 1, `count`)

            # Next selected item
            index = self.SelectedChaptersListCtrl.GetNextSelected(index-1)

        self.TestCardsCount.SetValue(`self.CardSet.GetTestCardsCount()`)
