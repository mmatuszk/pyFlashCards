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
# $File:$
# $Revision: 1.2 $
# $Date: 2006/10/29 23:28:26 $
# $Author: marcin $
#-------------------------------------------------------------------------------
import FlashCard
import wx

import wx.gizmos as gizmos

import events

ID_FLASH_CARD_DISP_FRAME = wx.NewId()

class FlashCardDataDispFrame(wx.Frame):
    def __init__(self, parent, id, CardSet):
        wx.Frame.__init__(self, parent, ID_FLASH_CARD_DISP_FRAME,
                          'Flash cards data display')

        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.CardSet = CardSet

        self.tree = gizmos.TreeListCtrl(self, -1, style = wx.TR_DEFAULT_STYLE
                                                    | wx.TR_FULL_ROW_HIGHLIGHT) 

        self.tree.AddColumn('Main column')
        self.tree.AddColumn('Front text')
        self.tree.AddColumn('Back text')
        self.tree.SetMainColumn(0)

        self.root = self.tree.AddRoot('Card set')

        self.Chapters = self.tree.AppendItem(self.root, "Chapters")
        self.AvailableChapters = self.tree.AppendItem(self.root,
                                                    "Availalbe Chapters")
        self.SelectedChapters = self.tree.AppendItem(self.root,
                                                    "Selected Chapters")
        self.Cards = self.tree.AppendItem(self.root, 'Cards')
        self.Boxes = self.tree.AppendItem(self.root, 'Boxes')
        self.TestCard = self.tree.AppendItem(self.Boxes, 'Test card')
        self.Box = []
        for box in self.CardSet.GetBoxes():
            self.Box.append(self.tree.AppendItem(self.Boxes, 
                                                 'Box %d' % box.GetId()))

        self.Update()

        self.SetSize((600,600))

    def Update(self):
        print 'Update data display'
        self.UpdateChapters()
        self.UpdateAvailableChapters()
        self.UpdateSelectedChapters()
        self.UpdateCards()
        self.UpdateBoxes()

    def OnSize(self, event):
        size = self.GetClientSize()
        self.tree.SetSize(size)
        width = size[0]
        self.tree.SetColumnWidth(0, width/3)
        self.tree.SetColumnWidth(1, width/3)
        self.tree.SetColumnWidth(2, width/3)

    def UpdateChapters(self):
        self.tree.DeleteChildren(self.Chapters)
        for chapter in self.CardSet.GetChapters():
            item = self.tree.AppendItem(self.Chapters, chapter)
            self.tree.SetItemText(item, self.CardSet.GetChapterLabel(chapter), 1)

    def UpdateAvailableChapters(self):
        self.tree.DeleteChildren(self.AvailableChapters)
        for chapter in self.CardSet.GetAvailableChapters():
            self.tree.AppendItem(self.AvailableChapters, chapter)

    def UpdateSelectedChapters(self):
        self.tree.DeleteChildren(self.SelectedChapters)
        for chapter in self.CardSet.GetSelectedChapters():
            self.tree.AppendItem(self.SelectedChapters, chapter)

    def UpdateCards(self):
        self.tree.DeleteChildren(self.Cards)
        for chapter in self.CardSet.GetChapters():
            ch = self.tree.AppendItem(self.Cards, chapter)
            cards = self.CardSet.GetChapterCards(chapter)
            i = 0
            for c in cards:
                child = self.tree.AppendItem(ch, 'Card %d' % i)
                self.tree.SetItemText(child, c.GetFrontText(), 1)
                self.tree.SetItemText(child, c.GetBackText(), 2)
                i+=1

    def UpdateBoxes(self):
        card = self.CardSet.GetTestCard()
        if card == None:
            self.tree.SetItemText(self.TestCard, "", 1)
            self.tree.SetItemText(self.TestCard, "", 2)
        else:
            self.tree.SetItemText(self.TestCard, card.GetFrontText(), 1)
            self.tree.SetItemText(self.TestCard, card.GetBackText(), 2)

        for BoxData, BoxItem in zip (self.CardSet.GetBoxes(), self.Box):
            self.tree.SetItemText(BoxItem, '%d' % BoxData.GetCardCount(), 1)
            self.tree.SetItemText(BoxItem, '%d' % BoxData.GetCapacity(), 2)
            self.tree.DeleteChildren(BoxItem)
            for c in BoxData.GetCards():
                child = self.tree.AppendItem(BoxItem, "Card")
                self.tree.SetItemText(child, c.GetFrontText(), 1)
                self.tree.SetItemText(child, c.GetBackText(), 2)

    def OnClose(self, event):
        evt = events.WindowClosedEvent(events.myEVT_WINDOW_CLOSED, self.GetId())
        self.GetEventHandler().ProcessEvent(evt)
        print "Sending event"
        self.Destroy()
