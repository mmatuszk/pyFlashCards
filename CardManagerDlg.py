#Bboa:Dialog:CardManagerDlg
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
# $Source: /cvsroot/pyflashcards/pyFlashCards/CardManagerDlg.py,v $
# $Revision: 1.9 $
# $Date: 2008/10/04 21:29:51 $
# $Author: marcin $
#-------------------------------------------------------------------------------
import wx
import wx.lib.imagebrowser as ib
import TextHtmlCtrl as th

import FlashCard
import shutil, os

MaxPopupChapters = 100

def create(parent):
    return CardManagerDlg(parent)

[wxID_CARDMANAGERDLG, wxID_CARDMANAGERDLGBACKENTRY, 
 wxID_CARDMANAGERDLGBACKIMAGEBUTTON, wxID_CARDMANAGERDLGCARDCOUNT, 
 wxID_CARDMANAGERDLGCARDDOWNBTN, wxID_CARDMANAGERDLGCARDLISTCTRL, 
 wxID_CARDMANAGERDLGCARDUPBTN, wxID_CARDMANAGERDLGCHAPTERSCHOICE, 
 wxID_CARDMANAGERDLGCOMMITCARDBTN, wxID_CARDMANAGERDLGCANCELCARDBTN, 
 wxID_CARDMANAGERDLGFINDNEXTBTN, wxID_CARDMANAGERDLGFINDPREVIOUSBTN, 
 wxID_CARDMANAGERDLGFINDTEXTCTRL, wxID_CARDMANAGERDLGFRONTENTRY, 
 wxID_CARDMANAGERDLGFRONTIMAGEBUTTON, 
 wxID_CARDMANAGERDLGREMOVEBACKIMAGEBUTTON, 
 wxID_CARDMANAGERDLGREMOVEFRONTIMAGEBUTTON, wxID_CARDMANAGERDLGSTATICTEXT1, 
 wxID_CARDMANAGERDLGSTATICTEXT2, wxID_CARDMANAGERDLGSTATICTEXT3, 
 wxID_CARDMANAGERDLGSTATICTEXT4, wxID_CARDMANAGERDLGSTATICTEXT5, 
] = [wx.NewId() for _init_ctrls in range(22)]

hspacer = (10,1)

class CardManagerDlg(wx.Dialog):
    def MakeChaptersUI(self, parent):
        chapterlabel = wx.StaticText(parent, -1, 'Chapters')
        self.ChaptersChoice = wx.Choice(choices=[],
              id=wxID_CARDMANAGERDLGCHAPTERSCHOICE, name=u'ChaptersChoice',
              parent=self, style=0)
        self.ChaptersChoice.Bind(wx.EVT_CHOICE, self.OnChaptersChoiceChoice,
              id=wxID_CARDMANAGERDLGCHAPTERSCHOICE)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(chapterlabel, 0, wx.ALIGN_CENTER)
        sizer.AddSpacer(hspacer)
        sizer.Add(self.ChaptersChoice, 1, wx.ALIGN_CENTER | wx.EXPAND)

        return sizer

    def MakeEntryUI(self, parent):
        self.FrontEntry = th.TextHtmlCtrl(id=wxID_CARDMANAGERDLGFRONTENTRY,
              name=u'FrontEntry', parent=self, style=wx.TE_MULTILINE,
              value=u'')
        frontlabel = wx.StaticText( label=u'Front', parent=self,
              style=0)

        self.BackEntry = th.TextHtmlCtrl(id=wxID_CARDMANAGERDLGBACKENTRY,
              name=u'BackEntry', parent=self, 
              style=wx.TE_MULTILINE,
              value=u'')
        backlabel = wx.StaticText(label=u'Back', parent=self,
              style=0)

        self.CommitCardBtn = wx.Button(parent, wxID_CARDMANAGERDLGCOMMITCARDBTN,
                'Commit Card')
        self.CommitCardBtn.Bind(wx.EVT_BUTTON, self.OnCommitCardBtnButton,
              id=wxID_CARDMANAGERDLGCOMMITCARDBTN)

        self.CancelCardBtn = wx.Button(parent, wxID_CARDMANAGERDLGCANCELCARDBTN,
                'Cancel Changes')
        self.CancelCardBtn.Bind(wx.EVT_BUTTON, self.OnCancelChangesButton,
              id=wxID_CARDMANAGERDLGCANCELCARDBTN)

        self.FrontImageButton = wx.BitmapButton(bitmap=wx.NullBitmap,
              id=wxID_CARDMANAGERDLGFRONTIMAGEBUTTON, name=u'FrontImageButton',
              parent=self, size=wx.Size(120, 120),
              style=wx.BU_AUTODRAW)
        self.FrontImageButton.Bind(wx.EVT_BUTTON, self.OnFrontImageButtonButton,
              id=wxID_CARDMANAGERDLGFRONTIMAGEBUTTON)

        self.BackImageButton = wx.BitmapButton(bitmap=wx.NullBitmap,
              id=wxID_CARDMANAGERDLGBACKIMAGEBUTTON, name=u'BackImageButton',
              parent=self, size=wx.Size(120, 120),
              style=wx.BU_AUTODRAW)
        self.BackImageButton.Bind(wx.EVT_BUTTON, self.OnBackImageButtonButton,
              id=wxID_CARDMANAGERDLGBACKIMAGEBUTTON)

        self.RemoveFrontImageButton = wx.Button(
              id=wxID_CARDMANAGERDLGREMOVEFRONTIMAGEBUTTON,
              label=u'Remove Image', name=u'RemoveFrontImageButton',
              parent=self, style=0)
        self.RemoveFrontImageButton.Bind(wx.EVT_BUTTON,
              self.OnRemoveFrontImageButtonButton,
              id=wxID_CARDMANAGERDLGREMOVEFRONTIMAGEBUTTON)

        self.RemoveBackImageButton = wx.Button(
              id=wxID_CARDMANAGERDLGREMOVEBACKIMAGEBUTTON,
              label=u'Remove Image', name=u'RemoveBackImageButton',
              parent=self, style=0)
        self.RemoveBackImageButton.Bind(wx.EVT_BUTTON,
              self.OnRemoveBackImageButtonButton,
              id=wxID_CARDMANAGERDLGREMOVEBACKIMAGEBUTTON)

        sizer = wx.BoxSizer(wx.VERTICAL)

        # entry sizer: front
        entry_sizer_row = wx.BoxSizer(wx.HORIZONTAL)
        entry_sizer_img = wx.BoxSizer(wx.VERTICAL)

        entry_sizer_img.Add(self.FrontImageButton, 0, wx.ALIGN_CENTER)
        entry_sizer_img.Add(self.RemoveFrontImageButton, 0, wx.ALIGN_CENTER)

        entry_sizer_row.Add(frontlabel, 0, wx.ALIGN_TOP)
        entry_sizer_row.AddSpacer(hspacer)
        entry_sizer_row.Add(self.FrontEntry, 1, wx.EXPAND)
        entry_sizer_row.Add(entry_sizer_img, 0, wx.ALIGN_CENTER)
        
        sizer.Add(entry_sizer_row, 1, wx.EXPAND)
        sizer.AddSpacer((1, 15))

        # entry sizer: back
        entry_sizer_row = wx.BoxSizer(wx.HORIZONTAL)
        entry_sizer_img = wx.BoxSizer(wx.VERTICAL)

        entry_sizer_img.Add(self.BackImageButton, 0, wx.ALIGN_CENTER)
        entry_sizer_img.Add(self.RemoveBackImageButton, 0, wx.ALIGN_CENTER)

        entry_sizer_row.Add(backlabel, 0, wx.ALIGN_TOP)
        entry_sizer_row.AddSpacer(hspacer)
        entry_sizer_row.Add(self.BackEntry, 1, wx.EXPAND)
        entry_sizer_row.Add(entry_sizer_img, 0, wx.ALIGN_CENTER)

        sizer.Add(entry_sizer_row, 1, wx.EXPAND)

        # entry sizer: commit/cancel
        entry_sizer_row = wx.BoxSizer(wx.HORIZONTAL)
        entry_sizer_row.Add(self.CommitCardBtn)
        entry_sizer_row.Add(self.CancelCardBtn)

        sizer.Add(entry_sizer_row, 0, wx.ALIGN_CENTER)

        return sizer

    def MakeFindUI(self, parent):
        findlabel = wx.StaticText(parent, -1, 'Find')

        self.FindTextCtrl = wx.TextCtrl(parent, wxID_CARDMANAGERDLGFINDTEXTCTRL,
            style=wx.TE_PROCESS_ENTER, value=u'')
        self.FindTextColourSearch = self.FindTextCtrl.GetBackgroundColour()
        self.FindTextColourFound = wx.Colour(200, 255, 0)
        self.FindTextColourNotFound = wx.Colour(255, 0, 65)

        self.FindTextCtrl.Bind(wx.EVT_TEXT_ENTER, self.OnFindNext)
        self.FindTextCtrl.Bind(wx.EVT_TEXT, self.OnFindText)

        self.FindNextBtn = wx.Button(id=wxID_CARDMANAGERDLGFINDNEXTBTN,
              label=u'Find Next', name=u'FindNextBtn', parent=self,
              style=0)
        self.FindNextBtn.Bind(wx.EVT_BUTTON, self.OnFindNext)

        self.FindPrevBtn = wx.Button(id=wxID_CARDMANAGERDLGFINDPREVIOUSBTN,
              label=u'FindPrev', name=u'FindPrevBtn', parent=self,
              style=0)
        self.FindPrevBtn.Bind(wx.EVT_BUTTON, self.OnFindPrev)

        sizer = wx.BoxSizer(wx.HORIZONTAL)

        sizer.Add(findlabel, 0, wx.ALIGN_CENTER)
        sizer.AddSpacer(hspacer)
        sizer.Add(self.FindTextCtrl, 0, wx.ALIGN_CENTER)
        sizer.AddSpacer(hspacer)
        sizer.Add(self.FindNextBtn, 0, wx.ALIGN_CENTER)
        sizer.Add(self.FindPrevBtn, 0, wx.ALIGN_CENTER)

        return sizer

    def MakeCardCountUI(self, parent):
        countlabel = wx.StaticText(label=u'Cards', parent=self,
              style=0)
        self.CardCount = wx.TextCtrl(id=wxID_CARDMANAGERDLGCARDCOUNT,
              name=u'CardCount', parent=self, 
              size=wx.Size(48, 21), style=wx.TE_READONLY, value=u'')

        sizer = wx.BoxSizer(wx.HORIZONTAL)

        sizer.Add(countlabel)
        sizer.AddSpacer(hspacer, 0, wx.ALIGN_CENTER)
        sizer.Add(self.CardCount, 0, wx.ALIGN_CENTER)

        return sizer

    def MakeCardListUI(self, parent):
        self.CardListCtrl = wx.ListCtrl(id=wxID_CARDMANAGERDLGCARDLISTCTRL,
              name=u'CardListCtrl', parent=self, 
              size=wx.Size(312, 624), style=wx.LC_REPORT)
        self.CardListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED,
              self.OnCardListCtrlListItemSelected,
              id=wxID_CARDMANAGERDLGCARDLISTCTRL)
        self.CardListCtrl.Bind(wx.EVT_LIST_ITEM_DESELECTED,
              self.OnCardListCtrlListItemDeselected,
              id=wxID_CARDMANAGERDLGCARDLISTCTRL)
        self.CardListCtrl.Bind(wx.EVT_CHAR, self.OnCardListCtrlChar)

        self.CardUpBtn = wx.Button(id=wxID_CARDMANAGERDLGCARDUPBTN, label=u'Up',
              name=u'CardUpBtn', parent=self, 
              style=0)

        self.CardDownBtn = wx.Button(id=wxID_CARDMANAGERDLGCARDDOWNBTN,
              label=u'Down', name=u'CardDownBtn', parent=self,
              style=0)

        sizer = wx.BoxSizer(wx.HORIZONTAL)

        mv_sizer = wx.BoxSizer(wx.VERTICAL)

        mv_sizer.Add(self.CardUpBtn, 0, wx.ALIGN_CENTER)
        mv_sizer.Add(self.CardDownBtn, 0, wx.ALIGN_CENTER)

        sizer.Add(self.CardListCtrl, 0, wx.EXPAND)
        sizer.Add(mv_sizer, 0, wx.ALIGN_CENTER)

        return sizer

    def MakeHelpUI(self, parent):
        HelpButton = wx.Button(parent, wx.ID_HELP)

        HelpButton.Bind(wx.EVT_BUTTON, self.OnHelp)

        return HelpButton

    def _init_ctrls(self, prnt):
        # This function was first generated using Boa constructor
        # I changed it, but kept a lot of code to save time so it looks
        # a bit strange
        wx.Dialog.__init__(self, id=wxID_CARDMANAGERDLG, 
              name=u'CardManagerDlg',
              parent=prnt, size=wx.Size(1100, 700),
              style=wx.TAB_TRAVERSAL | wx.DEFAULT_DIALOG_STYLE |
              wx.RESIZE_BORDER,
              title=u'Card Manager')

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        # Make entry before chapters to get focus on front entry
        entry_sizer = self.MakeEntryUI(self)
        ch_sizer = self.MakeChaptersUI(self)
        find_sizer = self.MakeFindUI(self)
        ct_sizer = self.MakeCardCountUI(self)
        list_sizer = self.MakeCardListUI(self)

        # col 1
        sizer_col = wx.BoxSizer(wx.VERTICAL)
        sizer_col.Add(ch_sizer, 0, wx.EXPAND)
        sizer_col.AddSpacer((1,15))
        sizer_col.Add(entry_sizer, 1, wx.EXPAND)
        sizer_col.Add(find_sizer)

        sizer.Add(sizer_col, 1, wx.EXPAND | wx.ALL, 10)

        # col 2
        sizer_col = wx.BoxSizer(wx.VERTICAL)
        sizer_col.Add(ct_sizer)
        sizer_col.Add(list_sizer, 1, wx.EXPAND)
        sizer_col.Add(self.MakeHelpUI(self), 0, wx.ALIGN_RIGHT)

        sizer.Add(sizer_col, 0, wx.EXPAND | wx.ALL, 10)


        self.SetSizer(sizer)

    def __init__(self, parent, CardSet, Config, help):
        # Call the boa generate function to initialize controls
        self._init_ctrls(parent)
        
        self.help = help
        self.CardSet = CardSet
        self.Config = Config

        self.ResetImageVars()

        # CardEditIndex is used to store the index of a card that is being
        # modified.  If a new card is being entered the value is set to < 0
        self.CardEditIndex = -1
        
        chapters = CardSet.GetChapters()
        
        for ch in chapters:
            self.ChaptersChoice.Append(ch)
            
        self.ChaptersChoice.SetSelection(0)
        
        self.InitCardEntry()
        
        width = self.CardListCtrl.GetSize()[0]/2-2
        self.CardListCtrl.InsertColumn(0, "Card Front", width = width)
        self.CardListCtrl.InsertColumn(1, "Card Back", width = width)
        
        self.AddCards2List(self.CardSet.GetChapterCards(chapters[0]))


        self.CardCount.SetValue(`self.CardSet.GetChapterCardCount(chapters[0])`)

        # for wxMSW
        self.CardListCtrl.Bind(wx.EVT_COMMAND_RIGHT_CLICK, self.OnRightClick)

        # for wxGTK
        self.CardListCtrl.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)

        # Bind the OnCloseWindow in order to check in edited cards is saved
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        # Dialog shortcuts
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

    def SelectCard(self, card):
        chapter = card.GetChapter()

        # Select chapter 
        self.ChaptersChoice.SetStringSelection(chapter)
        self.CardListCtrl.DeleteAllItems()
        self.AddCards2List(self.CardSet.GetChapterCards(chapter))

        # Select card for edit
        index = self.CardSet.GetCardIndex(card)
        self.CardListCtrl.SetItemState(index, wx.LIST_STATE_SELECTED,
                wx.LIST_STATE_SELECTED)

        # Display card
        self.DispCard(card)

        self.CardListCtrl.SetFocus()

        self.CardEditIndex = index
        
    def ResetImageVars(self):
        # Initialize variables associated with the front image
        self.FrontImage = None
        self.NewFrontImage = None
        self.FrontImageChanged = False
        # Initialize variables associated with the back image
        self.NewBackImage = None
        self.BackImage = None
        self.BackImageChanged = False

    def InitCardEntry(self):
        f = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL, False)
        print 'CardManger: ' + f.GetFaceName()
        self.FrontEntry.SetFont(f)
        self.BackEntry.SetFont(f)

        self.NoImageBitmap = wx.Image('icons/noimage.jpg', 
                wx.BITMAP_TYPE_JPEG).ConvertToBitmap()
        self.FrontImageButton.SetBitmapLabel(self.NoImageBitmap)
        self.BackImageButton.SetBitmapLabel(self.NoImageBitmap)

    def ResetCardUI(self):
        self.FrontEntry.Enable()
        self.BackEntry.Enable()
        self.CommitCardBtn.Enable()
        self.FrontImageButton.Enable()
        self.BackImageButton.Enable()

        self.FrontEntry.SetValue("")
        self.BackEntry.SetValue("")
        self.FrontImageButton.SetBitmapLabel(self.NoImageBitmap)
        self.BackImageButton.SetBitmapLabel(self.NoImageBitmap)

        self.UpdateCardCountUI()

        self.FrontEntry.SetFocus()

    def DispCard(self, card):
        FrontText = card.GetFrontText()
        BackText = card.GetBackText()
        self.FrontEntry.SetValue(FrontText)
        self.BackEntry.SetValue(BackText)
        self.FrontImage = card.GetFrontImage()
        self.BackImage = card.GetBackImage()
        if self.FrontImage:
            bsize = self.FrontImageButton.GetSize()
            self.FrontImageButton.SetBitmapLabel(
                    MakeButtonBitmap(self.FrontImage, bsize))
        else:
            self.FrontImageButton.SetBitmapLabel(self.NoImageBitmap)

        if self.BackImage:
            bsize = self.BackImageButton.GetSize()
            self.BackImageButton.SetBitmapLabel(
                    MakeButtonBitmap(self.BackImage, bsize))
        else:
            self.BackImageButton.SetBitmapLabel(self.NoImageBitmap)
        
    #---------------------------------------------------------------------------
    # Function: AddCards2List
    #
    # History:
    #   07/03/2005 : created
    # Action:
    #   Function appends a list of cards to the CardListCtrl.
    #---------------------------------------------------------------------------
    def AddCards2List(self, list):
        for card in list:
            front, back = card.GetBothSides()
            front = front.split('\n')[0]
            back = back.split('\n')[0]
            # Insert cards at the end of the list by getting the index from the
            # number of items in the list
            index = self.CardListCtrl.GetItemCount()
            self.CardListCtrl.InsertStringItem(index, front)            
            self.CardListCtrl.SetStringItem(index, 1, back)

    def MakeCardImage(self, src):
        dest = self.CardSet.GetNextImageName()
        shutil.copy(src, dest)
        return dest

    def OnCommitCardBtnButton(self, event):
        # Check if a new card is created or a existing card is edited
        if self.CardEditIndex < 0:
            # A new card is created
            # Get the card chapter
            chapter = self.ChaptersChoice.GetStringSelection()

            # Create a new card
            FrontText = self.FrontEntry.GetValue()
            BackText = self.BackEntry.GetValue()
            card = FlashCard.FlashCard(FrontText, BackText)
            if self.FrontImageChanged:
                card.SetFrontImage(self.MakeCardImage(self.NewFrontImage))
            if self.BackImageChanged:
                card.SetBackImage(self.MakeCardImage(self.NewBackImage))

            # Add the card to the card set
            self.CardSet.AddCard(chapter, card)
            
            # Show the new card in the card list
            self.AddCards2List([card])
        else:
            # An existing card is changed
            # Get the card chapter
            chapter = self.ChaptersChoice.GetStringSelection()
            index = self.CardEditIndex

            # Retrive the modified card
            card = self.CardSet.GetCardCopy(chapter, index)

            # Modify card text
            card.SetFrontText(self.FrontEntry.GetValue())
            card.SetBackText(self.BackEntry.GetValue())

            # Modify front image
            # Check if the front image changed
            if self.FrontImageChanged:
                # Check if there was an image at the start
                if self.FrontImage:
                    # If yes, check if there is a new image
                    if self.NewFrontImage:
                        # If yes, we need to remove the old image and set the
                        # new one
                        os.remove(self.FrontImage)
                        card.SetFrontImage(self.MakeCardImage(
                            self.NewFrontImage))
                    else:
                        # We need to remove the image
                        os.remove(self.FrontImage)
                        card.SetFrontImage(None)
                else:
                    # There was no image to begin with
                    if self.NewFrontImage:
                        # Create a new image
                        card.SetFrontImage(self.MakeCardImage(
                            self.NewFrontImage))
                    else:
                        # Nothing to do, an image was probably added and then
                        # removed
                        pass
            else:
                # If the image did not change, there is no need to do anything
                pass

            # Modify back image
            # Check if the back image changed
            if self.BackImageChanged:
                # Check if there was an image at the start
                if self.BackImage:
                    # If yes, check if there is a new image
                    if self.NewBackImage:
                        # If yes, we need to remove the old image and set the
                        # new one
                        os.remove(self.BackImage)
                        card.SetBackImage(self.MakeCardImage(
                            self.NewBackImage))
                    else:
                        # We need to remove the image
                        os.remove(self.BackImage)
                        card.SetBackImage(None)
                else:
                    # There was no image to begin with
                    if self.NewBackImage:
                        # Create a new image
                        card.SetBackImage(self.MakeCardImage(
                            self.NewBackImage))
                    else:
                        # Nothing to do, an image was probably added and then
                        # removed
                        pass
            else:
                # If the image did not change, there is no need to do anything
                pass

            # Update GUI controls
            self.CardListCtrl.SetStringItem(index, 0, 
                    card.GetFrontText().split('\n')[0])
            self.CardListCtrl.SetStringItem(index, 1, 
                    card.GetBackText().split('\n')[0])
            self.CardListCtrl.SetItemState(index, 0, wx.LIST_STATE_SELECTED)
            
            # Update program data
            self.CardSet.ModifyCard(chapter, index, card)
            
            # We are finished editing.
            self.CardEditIndex = -1

        # Reset all image variables
        self.ResetImageVars()

        # Reset UI
        self.ResetCardUI()

    def UpdateCardCountUI(self):
        chapter = self.ChaptersChoice.GetStringSelection()
        self.CardCount.SetValue(`self.CardSet.GetChapterCardCount(chapter)`)
        
    def CancelCardEdit(self):
        self.ResetCardUI()
        self.ResetImageVars()

    # Check if the edited card is modified
    def IsCardModified(self):
        if self.CardEditIndex < 0:
            if self.FrontEntry.GetValue() <> '':
                return True
            if self.BackEntry.GetValue() <> '':
                return True
            if self.FrontImageChanged or self.BackImageChanged:
                return True
        else:
            chapter = self.ChaptersChoice.GetStringSelection()
            index = self.CardEditIndex

            # Retrive the modified card
            card = self.CardSet.GetCard(chapter, index)

            if self.FrontEntry.GetValue() <> card.GetFrontText():
                return True
            if self.BackEntry.GetValue() <> card.GetBackText():
                return True
            if self.FrontImageChanged or self.BackImageChanged:
                return True

        return False

    def GetData(self):
        return self.CardSet, self.Config

    def DeleteSelectedCards(self):
        chapter = self.ChaptersChoice.GetStringSelection()
        index = self.CardListCtrl.GetFirstSelected()
        
        while index != -1:
            self.CardListCtrl.DeleteItem(index)
            self.CardSet.DeleteCard(chapter, index)
            index = self.CardListCtrl.GetNextSelected(index-1)

    def MoveSelectedCards(self, NewChapter):
        chapter = self.ChaptersChoice.GetStringSelection()
        index = self.CardListCtrl.GetFirstSelected()
        
        while index != -1:
            self.CardListCtrl.DeleteItem(index)
            self.CardSet.MoveCard(chapter, index, NewChapter)
            index = self.CardListCtrl.GetNextSelected(index-1)

        self.UpdateCardCountUI()

    def OnKeyDown(self, event):
        keycode = event.GetKeyCode()

        if event.ControlDown() and not event.ShiftDown() \
                and not event.AltDown():
            if keycode == ord('F'):
                self.FindTextCtrl.SetFocus()
                return

        event.Skip()

    def OnCancelChangesButton(self, event):
        index = self.CardEditIndex
        if index >= 0:
            self.CardListCtrl.SetItemState(index, 0, wx.LIST_STATE_SELECTED)

        self.CancelCardEdit()
        self.FrontEntry.SetFocus()
        
        self.CardEditIndex = -1

    def OnHelp(self, event):
        self.help.Display('Card Manager')

    def OnChaptersChoiceChoice(self, event):
        chapter = event.GetString()
        self.CardListCtrl.DeleteAllItems()
        self.AddCards2List(self.CardSet.GetChapterCards(chapter))
        self.ResetCardUI()
        self.UpdateCardCountUI()
        
    def OnCardListCtrlListItemSelected(self, event):
        index = event.GetIndex()
        if self.CardListCtrl.GetSelectedItemCount() == 1:
            self.FrontEntry.Enable()
            self.FrontImageButton.Enable()
            self.RemoveFrontImageButton.Enable()
            self.BackEntry.Enable()
            self.BackImageButton.Enable()
            self.RemoveBackImageButton.Enable()
            self.CommitCardBtn.Enable()
            chapter = self.ChaptersChoice.GetStringSelection()
            card = self.CardSet.GetCard(chapter, index)

            # Display the card
            self.DispCard(card)    

            self.CardEditIndex = index
        else:
            self.FrontEntry.SetValue('')
            self.FrontEntry.Disable()
            self.BackEntry.SetValue('')
            self.BackEntry.Disable()
            self.FrontImageButton.SetBitmapLabel(self.NoImageBitmap)
            self.FrontImageButton.Disable()
            self.BackImageButton.SetBitmapLabel(self.NoImageBitmap)
            self.BackImageButton.Disable()
            self.RemoveFrontImageButton.Disable()
            self.RemoveBackImageButton.Disable()
            self.CommitCardBtn.Disable()
            self.CardEditIndex = -1

    def OnCardListCtrlListItemDeselected(self, event):
        if self.CardListCtrl.GetSelectedItemCount() == 0:
            self.CancelCardEdit()
            self.CardEditIndex = -1

    def OnCardListCtrlChar(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_DELETE or keycode == wx.WXK_BACK:
            self.DeleteSelectedCards()
            self.ResetCardUI()
        else:
            event.Skip()

    def OnFrontImageButtonButton(self, event):
        dir = self.Config.get('directories', 'image_dir')
        dlg = ib.ImageDialog(self, dir)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetFile()
            
            # Update config
            self.Config.set('directories', 'image_dir', 
                    os.path.dirname(filename))

            self.NewFrontImage = filename
            self.FrontImageChanged = True

            # Create the bitmap for the button
            bsize = self.FrontImageButton.GetSize()

            self.FrontImageButton.SetBitmapLabel(
                    MakeButtonBitmap(self.NewFrontImage, bsize))

        dlg.Destroy()

    def OnBackImageButtonButton(self, event):
        dir = self.Config.get('directories', 'image_dir')
        dlg = ib.ImageDialog(self, dir)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetFile()
            
            # Update config
            self.Config.set('directories', 'image_dir', 
                    os.path.dirname(filename))

            self.NewBackImage = filename
            self.BackImageChanged = True

            # Create the bitmap for the button
            bsize = self.BackImageButton.GetSize()

            self.BackImageButton.SetBitmapLabel(
                    MakeButtonBitmap(self.NewBackImage, bsize))

        dlg.Destroy()

    def OnRemoveFrontImageButtonButton(self, event):
        self.NewFrontImage = None
        self.FrontImageChanged = True
        self.FrontImageButton.SetBitmapLabel(self.NoImageBitmap)

    def OnRemoveBackImageButtonButton(self, event):
        self.NewBackImage = None
        self.BackImageChanged = True
        self.BackImageButton.SetBitmapLabel(self.NoImageBitmap)

    def OnRightClick(self, event):
        # only do this part the first time so the events are only bound once
        if not hasattr(self, "popupIDDelete"):
            self.popupIDDelete = wx.NewId()
            self.popupIDMove = wx.NewId()
            self.popupIDChapters = [wx.NewId() for n in range(MaxPopupChapters)]

            self.Bind(wx.EVT_MENU, self.OnPopupDelete, id=self.popupIDDelete)
            self.Bind(wx.EVT_MENU, self.OnPopupMove, id=self.popupIDMove)
            for id in self.popupIDChapters:
                self.Bind(wx.EVT_MENU, self. OnPopupMoveChapter, id=id)

        # make a menu
        menu = wx.Menu()
        # add some items
        menu.Append(self.popupIDDelete, "Delete")

        sm = wx.Menu()
        self.PopupIDChapterMap = {}
        curChapter = self.ChaptersChoice.GetStringSelection()
        for chapter, id in zip(self.CardSet.GetChapters(), 
                self.popupIDChapters):
            if curChapter != chapter:
                sm.Append(id, chapter)
                self.PopupIDChapterMap[id] = chapter

        menu.AppendMenu(self.popupIDMove, "Move", sm)
        

        # Popup the menu.  If an item is selected then its handler
        # will be called before PopupMenu returns.
        #self.PopupMenu(menu, (self.x, self.y))
        self.PopupMenu(menu)
        menu.Destroy()

    def OnPopupDelete(self, event):
        self.DeleteSelectedCards()
        self.ResetCardUI()

    def OnPopupMove(self, event):
        event.Skip()

    def OnPopupMoveChapter(self, event):
        chapter = self.PopupIDChapterMap[event.GetId()]
        self.MoveSelectedCards(chapter)

    def OnCloseWindow(self, event):
        if self.IsCardModified():
            # A card is being edited
            dlg = wx.MessageDialog(self, 
                    "You are editing a card.  Do you really want to quit.", 
                    "Warning",
                    wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
            ans = dlg.ShowModal()
            dlg.Destroy()

        else:
            ans = wx.ID_YES

        if ans == wx.ID_YES:
            event.Skip()

    def OnFindText(self, event):
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

    def Find(self, str, case=False, direction=1):
        if len(self.cards) < 1:
            return

        found = False
        self.searchIndex = self.i + direction
        while not found and self.searchIndex <> self.i:
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

def MakeButtonBitmap(filename, bsize, pad=10):
        bw, bh = bsize
        filename = os.path.normpath(filename)
        print filename
        image = wx.Image(filename, wx.BITMAP_TYPE_ANY)
        iw, ih = image.GetWidth(), image.GetHeight()
        if iw >= ih:
            if iw > bw-pad:
                k = float(bw)/iw
            else:
                k = 1
        else:
            if ih > bw-pad:
                k = float(bh)/ih
            else:
                k = 1

        return image.Rescale(int(iw*k)-pad, int(ih*k)-pad).ConvertToBitmap()
