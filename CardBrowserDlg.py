#-------------------------------------------------------------------------------
# CardBrowserDlg.py
# Dialog for browsing cards in html mode
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

import wx
import wx.html as html
import FlashCard

CHAPTERS_CHOICE_ID  = wx.Window.NewControlId()
CARD_LIST_CTRL_ID   = wx.Window.NewControlId()

FIND_TEXT_ID = wx.Window.NewControlId()

FIND_NEXT_ID = wx.Window.NewControlId()
FIND_PREV_ID = wx.Window.NewControlId()

class CardBrowserDlg(wx.Dialog):
    def __init__(
            self, parent, ID, CardSet, Config, title='Card Browser', 
            size=(1024, 800), pos=wx.DefaultPosition, 
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER):
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
        self.Config = Config
        if Config:
            w = self.Config.getint('card_browser', 'width')
            h = self.Config.getint('card_browser', 'height')
            size = (w, h)

        print(size)
        wx.Dialog.__init__(self, id=ID, name='CardBrowserDlg',
              parent=parent, size=size, style=style, title=title)

        self.CardSet = CardSet
        self.cards = []
        self.i = 0
        self.searchIndex = -1

        self.SetMinSize((640, 480))

        # Now continue with the normal construction of the dialog
        # contents
        self.init_ctrls(parent)

        ch = self.ChaptersChoice.GetStringSelection()
        self.SelectChapter(ch)

        self.CardListCtrl.SetFocus()

        # Bind
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

    def init_ctrls(self, parent):
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Create it first so it gets focus when dlg is open
        self.CardListCtrl = wx.ListCtrl(self,
                CARD_LIST_CTRL_ID, size=(300,100),
                style=wx.LC_REPORT | wx.LC_SINGLE_SEL)

        # New line
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        chapterlabel = wx.StaticText(self, -1, 'Chapter:')

        self.ChaptersChoice = wx.Choice(self, CHAPTERS_CHOICE_ID,
                choices=self.CardSet.GetChapters())
        self.ChaptersChoice.SetSelection(0)


        hsizer.Add(chapterlabel, 0, wx.ALIGN_CENTER)
        #/hsizer.AddSpacer((5,5))
        hsizer.AddSpacer(5)
        hsizer.Add(self.ChaptersChoice, 1, wx.ALIGN_CENTER | wx.EXPAND)

        sizer.Add(hsizer, 0, wx.EXPAND)

        # New line
        hsizer = wx.BoxSizer(wx.HORIZONTAL)

        splitter = wx.SplitterWindow(self, -1)
        self.FrontDisp = html.HtmlWindow(splitter, -1, 
                style=wx.BORDER_SUNKEN | wx.HSCROLL)
        self.BackDisp = html.HtmlWindow(splitter, -1, 
                style=wx.BORDER_SUNKEN | wx.HSCROLL)

        
        splitter.SplitHorizontally(self.FrontDisp, self.BackDisp, 200)
        splitter.SetMinimumPaneSize(20)

        # Creation moved to the front so it gets focus when dlg is opened
        #self.CardListCtrl = wx.ListCtrl(self,
        #        CARD_LIST_CTRL_ID, size=(300,100),
        #        style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        width = self.CardListCtrl.GetSize()[0]/2-2
        self.CardListCtrl.InsertColumn(0, "Card Front", width = width)
        self.CardListCtrl.InsertColumn(1, "Card Back", width = width)

        hsizer.Add(splitter, 1, wx.EXPAND)
        hsizer.Add(self.CardListCtrl, 0, wx.EXPAND)

        sizer.Add(hsizer, 1, wx.EXPAND)

        # New line
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.IndexLabel=wx.StaticText(self, -1, 'Card')
        hsizer.Add(self.IndexLabel, 0)

        sizer.Add(hsizer, 0, wx.ALIGN_CENTER)

        # New line
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        prev = wx.Button(self, wx.ID_BACKWARD)
        next = wx.Button(self, wx.ID_FORWARD)

        hsizer.Add(prev, 0)
        #hsizer.AddSpacer((5,5))
        hsizer.AddSpacer((5))
        hsizer.Add(next, 0)

        sizer.Add(hsizer, 0, wx.ALIGN_CENTER)

        # New line
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        findlabel = wx.StaticText(self, -1, 'Find:')

        self.FindTextCtrl = wx.TextCtrl(self, FIND_TEXT_ID,
                style=wx.TE_PROCESS_ENTER)
        self.FindTextColourSearch = self.FindTextCtrl.GetBackgroundColour()
        self.FindTextColourFound = wx.Colour(200, 255, 0)
        self.FindTextColourNotFound = wx.Colour(255, 0, 65)

        up_bmp =  wx.ArtProvider.GetBitmap(wx.ART_GO_UP, wx.ART_BUTTON)
        down_bmp =  wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN, wx.ART_BUTTON)
        findnext = wx.BitmapButton(self, FIND_NEXT_ID,
                down_bmp)
        findprev = wx.BitmapButton(self, FIND_PREV_ID, up_bmp)

        hsizer.Add(findlabel, 0, wx.CENTER)
        #hsizer.AddSpacer((5,5))
        hsizer.AddSpacer(5)
        hsizer.Add(self.FindTextCtrl, 0, wx.CENTER)
        hsizer.Add(findnext, 0, wx.CENTER)
        hsizer.Add(findprev, 0, wx.CENTER)

        sizer.Add(hsizer)

        # Bind events
        next.Bind(wx.EVT_BUTTON, self.OnForward, id=wx.ID_FORWARD)
        prev.Bind(wx.EVT_BUTTON, self.OnBackward, id=wx.ID_BACKWARD)

        self.ChaptersChoice.Bind(wx.EVT_CHOICE, self.OnChaptersChoiceChoice,
              id=CHAPTERS_CHOICE_ID)

        self.CardListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED,
              self.OnCardListCtrlItemSelected,
              id=CARD_LIST_CTRL_ID)

        self.FindTextCtrl.Bind(wx.EVT_TEXT_ENTER, self.OnFindNext, 
                id = FIND_TEXT_ID)
        self.FindTextCtrl.Bind(wx.EVT_TEXT, self.OnFindText, 
                id = FIND_TEXT_ID)

        findnext.Bind(wx.EVT_BUTTON, self.OnFindNext, id=FIND_NEXT_ID)
        findprev.Bind(wx.EVT_BUTTON, self.OnFindPrev, id=FIND_NEXT_ID)


        self.SetSizer(sizer)

    def OnForward(self, event):
        if len(self.cards) < 1:
            return

        self.i += 1
        if self.i >= len(self.cards):
            self.i = 0

        card = self.cards[self.i]

        self.DisplayCard(card) 
        self.CardListCtrl.SetItemState(self.i, wx.LIST_STATE_SELECTED,
                wx.LIST_STATE_SELECTED)

        self.IndexLabel.SetLabel('Card %d/%d' % (self.i+1, len(self.cards)))

        self.CardListCtrl.SetFocus()

    def OnBackward(self, event):
        if len(self.cards) < 1:
            return

        self.i -= 1
        if self.i < 0:
            self.i = len(self.cards)-1

        card = self.cards[self.i]

        self.DisplayCard(card) 
        self.CardListCtrl.SetItemState(self.i, wx.LIST_STATE_SELECTED,
                wx.LIST_STATE_SELECTED)

        self.IndexLabel.SetLabel('Card %d/%d' % (self.i+1, len(self.cards)))

        self.CardListCtrl.SetFocus()

    def OnCardListCtrlItemSelected(self, event):
        self.i = event.GetIndex()
        card = self.cards[self.i]

        self.DisplayCard(card) 
        self.IndexLabel.SetLabel('Card %d/%d' % (self.i+1, len(self.cards)))

    def OnChaptersChoiceChoice(self, event):
        chapter = event.GetString()

        self.SelectChapter(chapter)

    def OnFindText(self, event):
        self.searchIndex = -1
        self.FindTextCtrl.SetBackgroundColour(self.FindTextColourSearch)
        event.Skip()

    def OnFindNext(self, event):
        searchStr = self.FindTextCtrl.GetValue()
        if searchStr == '':
            return
        i = self.Find(searchStr, False)
        if i > 0:
            card = self.cards[i]
            self.i = i
            self.DisplayCard(card) 
            self.CardListCtrl.SetItemState(self.i, wx.LIST_STATE_SELECTED,
                    wx.LIST_STATE_SELECTED)
            self.IndexLabel.SetLabel('Card %d/%d' % (self.i+1, len(self.cards)))
            self.FindTextCtrl.SetBackgroundColour(self.FindTextColourFound)
        else:
            self.FindTextCtrl.SetBackgroundColour(self.FindTextColourNotFound)

    def OnFindPrev(self, event):
        searchStr = self.FindTextCtrl.GetValue()
        if searchStr == '':
            return
        i = self.Find(searchStr, False, -1)
        if i > 0:
            card = self.cards[i]
            self.i = i
            self.DisplayCard(card) 
            self.CardListCtrl.SetItemState(self.i, wx.LIST_STATE_SELECTED,
                    wx.LIST_STATE_SELECTED)
            self.IndexLabel.SetLabel('Card %d/%d' % (self.i+1, len(self.cards)))
            self.FindTextCtrl.SetBackgroundColour(self.FindTextColourFound)
        else:
            self.FindTextCtrl.SetBackgroundColour(self.FindTextColourNotFound)

    def OnCloseWindow(self, event):
        if self.Config:
            w, h = self.GetSize()
            # Use str() for string conversion in Python 3
            self.Config.set('card_browser', 'width', str(w))
            self.Config.set('card_browser', 'height', str(h))
        event.Skip()
        
    def OnKeyDown(self, event):
        keycode = event.GetKeyCode()

        if event.ControlDown() and not event.ShiftDown() \
                and not event.AltDown():
            if keycode == ord('F'):
                self.FindTextCtrl.SetFocus()
                return

        event.Skip()

    def SelectChapter(self, chapter):
        self.cards = self.CardSet.GetChapterCards(chapter)
        self.i = 0

        if len(self.cards) < 1:
            self.FrontDisp.SetPage('<html></<html>')
            self.BackDisp.SetPage('<html></<html>')

            return

        card = self.cards[self.i]

        self.DisplayCard(card)

        self.CardListCtrl.DeleteAllItems()
        self.AddCards2List(self.cards)
        self.CardListCtrl.SetItemState(0, wx.LIST_STATE_SELECTED,
                wx.LIST_STATE_SELECTED)
        # Set focus
        self.CardListCtrl.SetFocus()

    def DisplayCard(self, card):
        face = self.CardSet.GetFrontFontFace()
        size = self.CardSet.GetFrontFontSize()
        self.FrontDisp.SetPage(card.GetFrontHtml(face, size))

        face = self.CardSet.GetBackFontFace()
        size = self.CardSet.GetBackFontSize()
        self.BackDisp.SetPage(card.GetBackHtml(face, size))
        self.IndexLabel.SetLabel('Card %d/%d' % (self.i+1, len(self.cards)))

    def Find(self, str, case=False, direction=1):
        if len(self.cards) < 1:
            return

        found = False
        self.searchIndex = self.i + direction
        while not found and self.searchIndex != self.i:
            card = self.cards[self.searchIndex]
            if card.FrontTextFind(str, case) >= 0 or\
                    card.BackTextFind(str, case) >= 0:
                found = True
            else:
                self.searchIndex += direction
                if self.searchIndex >= len(self.cards):
                    self.searchIndex = 0
                elif self.searchIndex < 0:
                    self.searchIndex = len(self.cards)-1

        if found:
            return self.searchIndex

        return -1

    def AddCards2List(self, list):
        for card in list:
            front, back = card.GetBothSides()
            front = front.split('\n')[0]
            back = back.split('\n')[0]
            
            # Insert cards at the end of the list by getting the index from the
            # number of items in the list
            index = self.CardListCtrl.GetItemCount()

            # Insert the front text
            self.CardListCtrl.InsertItem(index, front)

            # Set the back text in the second column
            self.CardListCtrl.SetItem(index, 1, back)
