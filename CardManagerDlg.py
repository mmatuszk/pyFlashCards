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
# $Revision: 1.16 $
# $Date: 2008/12/10 15:42:46 $
# $Author: marcin201 $
#-------------------------------------------------------------------------------
import wx
import wx.lib.imagebrowser as ib
import TextHtmlCtrl as th
import HTMLStrippingParser
import FlashCard
import AutoCorrDlg
import shutil, os

MaxPopupChapters = 100

def create(parent):
    return CardManagerDlg(parent)

ID_CMDLG                    = wx.NewId()
ID_CMDLG_BACKENTRY          = wx.NewId()
ID_CMDLG_BACKIMAGEBTN       = wx.NewId()
ID_CMDLG_CARDCOUNT          = wx.NewId()
ID_CMDLG_CARDDOWNBTN        = wx.NewId()
ID_CMDLG_CARDLISTCTRL       = wx.NewId()
ID_CMDLG_CARDUPBTN          = wx.NewId()
ID_CMDLG_CHAPTERSCHOICE     = wx.NewId()
ID_CMDLG_COMMITCARDBTN      = wx.NewId()
ID_CMDLG_CANCELCARDBTN      = wx.NewId()
ID_CMDLG_FINDNEXTBTN        = wx.NewId()
ID_CMDLG_FINDPREVIOUSBTN    = wx.NewId()
ID_CMDLG_SEARCHCTRL         = wx.NewId()
ID_CMDLG_FRONTENTRY         = wx.NewId()
ID_CMDLG_FRONTIMAGEBUTTON   = wx.NewId()
ID_CMDLG_REMOVEBACKIMAGEBTN = wx.NewId()
ID_CMDLG_REMOVEFRONTIMAGEBTN= wx.NewId()
ID_CMDLG_STATICTEXT1        = wx.NewId()
ID_CMDLG_STATICTEXT2        = wx.NewId()
ID_CMDLG_STATICTEXT3        = wx.NewId()
ID_CMDLG_STATICTEXT4        = wx.NewId()
ID_CMDLG_STATICTEXT5        = wx.NewId()
ID_CMDLG_AUTOCORRBTN        = wx.NewId()

hspacer = (10,1)
vspacer = (1, 10)

class CardManagerDlg(wx.Dialog):
    def MakeChaptersUI(self, parent):
        chapterlabel = wx.StaticText(parent, -1, 'Chapters')
        self.ChaptersChoice = wx.Choice(choices=[],
              id=ID_CMDLG_CHAPTERSCHOICE, name=u'ChaptersChoice',
              parent=self, style=0)
        self.ChaptersChoice.Bind(wx.EVT_CHOICE, self.OnChaptersChoiceChoice,
              id=ID_CMDLG_CHAPTERSCHOICE)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(chapterlabel, 0, wx.ALIGN_CENTER)
        sizer.AddSpacer(hspacer)
        sizer.Add(self.ChaptersChoice, 1, wx.ALIGN_CENTER | wx.EXPAND)

        return sizer

    def MakeEntryUI(self, parent):
        self.FrontEntry = th.TextHtmlCtrl(id=ID_CMDLG_FRONTENTRY,
              name=u'FrontEntry', parent=self, style=wx.TE_MULTILINE,
              value=u'', autocorr=self.autocorr)
        frontlabel = wx.StaticText( label=u'Front', parent=self,
              style=0)

        self.BackEntry = th.TextHtmlCtrl(id=ID_CMDLG_BACKENTRY,
              name=u'BackEntry', parent=self, 
              style=wx.TE_MULTILINE,
              value=u'', autocorr=self.autocorr)
        backlabel = wx.StaticText(label=u'Back', parent=self,
              style=0)

        self.CommitCardBtn = wx.Button(parent, ID_CMDLG_COMMITCARDBTN,
                'Commit Card')
        self.CommitCardBtn.Bind(wx.EVT_BUTTON, self.OnCommitCardBtnButton,
              id=ID_CMDLG_COMMITCARDBTN)

        self.CancelCardBtn = wx.Button(parent, ID_CMDLG_CANCELCARDBTN,
                'Cancel Changes')
        self.CancelCardBtn.Bind(wx.EVT_BUTTON, self.OnCancelChangesButton,
              id=ID_CMDLG_CANCELCARDBTN)

        self.FrontImageButton = wx.BitmapButton(bitmap=wx.NullBitmap,
              id=ID_CMDLG_FRONTIMAGEBUTTON, name=u'FrontImageButton',
              parent=self, size=wx.Size(120, 120),
              style=wx.BU_AUTODRAW)
        self.FrontImageButton.Bind(wx.EVT_BUTTON, self.OnFrontImageButtonButton,
              id=ID_CMDLG_FRONTIMAGEBUTTON)

        self.BackImageButton = wx.BitmapButton(bitmap=wx.NullBitmap,
              id=ID_CMDLG_BACKIMAGEBTN, name=u'BackImageButton',
              parent=self, size=wx.Size(120, 120),
              style=wx.BU_AUTODRAW)
        self.BackImageButton.Bind(wx.EVT_BUTTON, self.OnBackImageButtonButton,
              id=ID_CMDLG_BACKIMAGEBTN)

        self.RemoveFrontImageButton = wx.Button(
              id=ID_CMDLG_REMOVEFRONTIMAGEBTN,
              label=u'Remove Image', name=u'RemoveFrontImageButton',
              parent=self, style=0)
        self.RemoveFrontImageButton.Bind(wx.EVT_BUTTON,
              self.OnRemoveFrontImageButtonButton,
              id=ID_CMDLG_REMOVEFRONTIMAGEBTN)

        self.RemoveBackImageButton = wx.Button(
              id=ID_CMDLG_REMOVEBACKIMAGEBTN,
              label=u'Remove Image', name=u'RemoveBackImageButton',
              parent=self, style=0)
        self.RemoveBackImageButton.Bind(wx.EVT_BUTTON,
              self.OnRemoveBackImageButtonButton,
              id=ID_CMDLG_REMOVEBACKIMAGEBTN)

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
        entry_sizer_row.Add(self.CommitCardBtn, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        entry_sizer_row.Add(self.CancelCardBtn, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        sizer.Add(entry_sizer_row, 0, wx.ALIGN_CENTER)

        return sizer

    def MakeFindUI(self, parent):
        self.SearchCtrl = wx.SearchCtrl(parent, ID_CMDLG_SEARCHCTRL, style = wx.TE_PROCESS_ENTER)
        size = self.SearchCtrl.GetSize()
        size[0] *= 2
        self.SearchCtrl.SetInitialSize(size)

        self.FindTextColourSearch = self.SearchCtrl.GetBackgroundColour()
        self.FindTextColourFound = wx.Colour(200, 255, 0)
        self.FindTextColourNotFound = wx.Colour(255, 0, 65)

        self.SearchCtrl.Bind(wx.EVT_TEXT_ENTER, self.OnFindNext)
        self.SearchCtrl.Bind(wx.EVT_TEXT, self.OnFindNext)

        self.FindNextBtn = wx.Button(id=ID_CMDLG_FINDNEXTBTN,
              label=u'Find Next', name=u'FindNextBtn', parent=self,
              style=0)
        self.FindNextBtn.Bind(wx.EVT_BUTTON, self.OnFindNext)

        self.FindPrevBtn = wx.Button(id=ID_CMDLG_FINDPREVIOUSBTN,
              label=u'FindPrev', name=u'FindPrevBtn', parent=self,
              style=0)
        self.FindPrevBtn.Bind(wx.EVT_BUTTON, self.OnFindPrev)

        self.FindMessage = wx.StaticText(parent, -1, ' ')
        font = self.FindMessage.GetFont()
        font.SetWeight(wx.BOLD)
        self.FindMessage.SetFont(font)
        self.FindMessage.SetForegroundColour(wx.Color(94, 122, 167))

        h_sizer = wx.BoxSizer(wx.HORIZONTAL)

        h_sizer.Add(self.SearchCtrl, 0, wx.ALIGN_TOP)
        h_sizer.Add(self.FindNextBtn, 0, wx.ALIGN_TOP | wx.LEFT, 10)
        h_sizer.Add(self.FindPrevBtn, 0, wx.ALIGN_TOP | wx.LEFT, 10) 
        h_sizer.Add(self.FindMessage, 0, wx.ALIGN_CENTER | wx.LEFT, 20)

        return h_sizer

    def MakeCardCountUI(self, parent):
        countlabel = wx.StaticText(label=u'Cards', parent=self,
              style=0)
        self.CardCount = wx.TextCtrl(id=ID_CMDLG_CARDCOUNT,
              name=u'CardCount', parent=self, 
              size=wx.Size(48, 21), style=wx.TE_READONLY, value=u'')

        sizer = wx.BoxSizer(wx.HORIZONTAL)

        sizer.Add(countlabel)
        sizer.AddSpacer(hspacer, 0, wx.ALIGN_CENTER)
        sizer.Add(self.CardCount, 0, wx.ALIGN_CENTER)

        return sizer

    def MakeCardListUI(self, parent):
        if wx.Platform == '__WXGTK__':
            style = wx.LC_REPORT | wx.BORDER_SUNKEN
        else:
            style = wx.LC_REPORT
        self.CardListCtrl = wx.ListCtrl(id=ID_CMDLG_CARDLISTCTRL,
              name=u'CardListCtrl', parent=self, 
              size=wx.Size(300, 100), style= style)
        self.CardListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED,
              self.OnCardListCtrlListItemSelected,
              id=ID_CMDLG_CARDLISTCTRL)
        self.CardListCtrl.Bind(wx.EVT_LIST_ITEM_DESELECTED,
              self.OnCardListCtrlListItemDeselected,
              id=ID_CMDLG_CARDLISTCTRL)
        self.CardListCtrl.Bind(wx.EVT_CHAR, self.OnCardListCtrlChar)

        self.CardUpBtn = wx.Button(id=ID_CMDLG_CARDUPBTN, label=u'Up',
              name=u'CardUpBtn', parent=self, 
              style=0)
        self.CardUpBtn.Bind(wx.EVT_BUTTON, self.OnCardsUp,
              id=ID_CMDLG_CARDUPBTN)

        self.CardDownBtn = wx.Button(id=ID_CMDLG_CARDDOWNBTN,
              label=u'Down', name=u'CardDownBtn', parent=self,
              style=0)
        self.CardDownBtn.Bind(wx.EVT_BUTTON, self.OnCardsDown,
              id=ID_CMDLG_CARDDOWNBTN)

        sizer = wx.BoxSizer(wx.HORIZONTAL)

        mv_sizer = wx.BoxSizer(wx.VERTICAL)

        mv_sizer.Add(self.CardUpBtn, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        mv_sizer.Add(self.CardDownBtn, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        sizer.Add(self.CardListCtrl, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(mv_sizer, 0, wx.ALIGN_CENTER)

        return sizer

    def MakeHelpAutoCorrUI(self, parent):
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        AutoCorrButton = wx.Button(parent, ID_CMDLG_AUTOCORRBTN, 'AutoCorr')
        HelpButton = wx.Button(parent, wx.ID_HELP)

        sizer.Add(AutoCorrButton, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        sizer.Add(HelpButton, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        AutoCorrButton.Bind(wx.EVT_BUTTON, self.OnAutoCorr)
        HelpButton.Bind(wx.EVT_BUTTON, self.OnHelp)

        return sizer


    def _init_ctrls(self, prnt, size):
        # This function was first generated using Boa constructor
        # I changed it, but kept a lot of code to save time so it looks
        # a bit strange
        wx.Dialog.__init__(self, id=ID_CMDLG, 
              name=u'CardManagerDlg',
              parent=prnt, size=size,
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
        sizer_col.Add(find_sizer, 0, wx.ALIGN_LEFT)

        sizer.Add(sizer_col, 1, wx.EXPAND | wx.ALL, 10)

        # col 2
        sizer_col = wx.BoxSizer(wx.VERTICAL)
        sizer_col.Add(ct_sizer)
        sizer_col.Add(list_sizer, 1, wx.EXPAND)
        sizer_col.Add(self.MakeHelpAutoCorrUI(self), 0, wx.ALIGN_RIGHT)

        sizer.Add(sizer_col, 0, wx.EXPAND | wx.ALL, 10)


        self.SetSizer(sizer)

    def __init__(self, parent, CardSet, Config, autocorr, help, runtimepath, size=(1024, 700)):
        self.help = help
        self.runtimepath = runtimepath
        self.autocorr = autocorr
        self.CardSet = CardSet
        self.Config = Config
        if Config:
            w = self.Config.getint('card_browser', 'width')
            h = self.Config.getint('card_browser', 'height')
            size = (w, h)

        # Initialize search functionality
        self.lastSearchStr = ''
        self.searchCardIndex = -1

        # Call the boa generate function to initialize controls
        self._init_ctrls(parent, size)
        
        self.ResetImageVars()

        # CardEditIndex is used to store the index of a card that is being
        # modified.  If a new card is being entered the value is set to < 0
        self.CardEditIndex = -1
        
        chapters = CardSet.GetChapters()
        
        for ch in chapters:
            self.ChaptersChoice.Append(ch)
            
        self.ChaptersChoice.SetSelection(0)
        
        self.InitCardEntry()
        
        width = self.CardListCtrl.GetSize()[0]/2-5
        self.CardListCtrl.InsertColumn(0, "Card Front", width = width)
        self.CardListCtrl.InsertColumn(1, "Card Back", width = width)
        
        self.AddCards2ListUI(self.CardSet.GetChapterCards(chapters[0]))


        self.CardCount.SetValue(`self.CardSet.GetChapterCardCount(chapters[0])`)

        # for wxMSW
        self.CardListCtrl.Bind(wx.EVT_COMMAND_RIGHT_CLICK, self.OnRightClick)

        # for wxGTK
        self.CardListCtrl.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)

        # Bind the OnCloseWindow in order to
        #   1. check in edited cards is saved
        #   2. save current window size
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        # Dialog shortcuts
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

    def SelectCard(self, card):
        chapter = card.GetChapter()

        # Select chapter 
        self.ChaptersChoice.SetStringSelection(chapter)
        self.CardListCtrl.DeleteAllItems()
        self.AddCards2ListUI(self.CardSet.GetChapterCards(chapter))

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

        iconfile = os.path.join(self.runtimepath, 'icons/noimage.jpg')
        self.NoImageBitmap = wx.Image(iconfile, 
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
    # Function: AddCards2ListUI
    #
    # History:
    #   07/03/2005 : created
    # Action:
    #   Function appends a list of cards to the CardListCtrl.
    #---------------------------------------------------------------------------
    def AddCards2ListUI(self, list):
        for card in list:
            front = card.GetFrontFirstLineNoHtml()
            back = card.GetBackFirstLineNoHtml()
            # Insert cards at the end of the list by getting the index from the
            # number of items in the list
            index = self.CardListCtrl.GetItemCount()
            self.CardListCtrl.InsertStringItem(index, front)            
            self.CardListCtrl.SetStringItem(index, 1, back)

    
    # Insert a card to list UI at the index position
    def InsertCard2ListUI(self, index, card):
        front = card.GetFrontFirstLineNoHtml()
        back = card.GetBackFirstLineNoHtml()
        # Insert cards at the end of the list by getting the index from the
        # number of items in the list
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
            self.AddCards2ListUI([card])
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
                    card.GetFrontFirstLineNoHtml())
            self.CardListCtrl.SetStringItem(index, 1, 
                    card.GetBackFirstLineNoHtml())
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
        return self.CardSet, self.Config, self.autocorr

    def InsertNewCardAbove(self):
        # get info about selected card
        chapter = self.ChaptersChoice.GetStringSelection()
        index = self.CardListCtrl.GetFirstSelected()
        if index < 0:
            return

        # deselect the card
        i = index
        while i != -1:
            self.CardListCtrl.SetItemState(i, 0, wx.LIST_STATE_SELECTED)
            i = self.CardListCtrl.GetNextSelected(i)

        # Insert a new card into the card set
        self.CardSet.InsertNewCardAbove(chapter, index)

        # Update the state of the card list control
        self.CardListCtrl.InsertStringItem(index, "")            
        self.CardListCtrl.SetStringItem(index, 1, "")
        self.CardListCtrl.SetItemState(index, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)

    def InsertNewCardBelow(self):
        # get info about selected card
        chapter = self.ChaptersChoice.GetStringSelection()

        index = self.CardListCtrl.GetFirstSelected()
        if index < 0:
            return

        # find last selected card and deselect all cards at the same time
        # when done, index will point to last selected card
        i = index
        while i != -1:
            self.CardListCtrl.SetItemState(index, 0, wx.LIST_STATE_SELECTED)
            i = self.CardListCtrl.GetNextSelected(i)
            if i > 0:
                index = i

        # Insert a new card into the card set
        self.CardSet.InsertNewCardBelow(chapter, index)

        # Update the state of the card list control
        self.CardListCtrl.InsertStringItem(index+1, "")            
        self.CardListCtrl.SetStringItem(index+1, 1, "")
        self.CardListCtrl.SetItemState(index+1, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)

    def CardsUp(self):
        # get info about selected card
        chapter = self.ChaptersChoice.GetStringSelection()
        first = self.CardListCtrl.GetFirstSelected()
        # if no cards are selected or we are already at the top of the list, exit 
        if first < 1:
            return

        card = self.CardSet.GetCard(chapter, first-1)
        # find last selected cards
        i = first
        last = first
        while i != -1:
            i = self.CardListCtrl.GetNextSelected(i)
            if i > 0:
                last = i

        # move cards around in the card set
        self.CardSet.MoveCardsUp(chapter, first, last)

        # update the state of the card list control
        self.CardListCtrl.DeleteItem(first-1)
        self.InsertCard2ListUI(last, card)

    def CardsDown(self):
        # get info about selected card
        chapter = self.ChaptersChoice.GetStringSelection()
        first = self.CardListCtrl.GetFirstSelected()
        # if no cards are selected, exit 
        if first < 0:
            return

        # find last selected cards
        i = first
        last = first
        while i != -1:
            i = self.CardListCtrl.GetNextSelected(i)
            if i > 0:
                last = i

        # if we are at the end of the list, exit
        if last+1 == self.CardListCtrl.GetItemCount():
            return

        card = self.CardSet.GetCard(chapter, last+1)

        # move cards around in the card set
        self.CardSet.MoveCardsDown(chapter, first, last)

        # update the state of the card list control
        self.CardListCtrl.DeleteItem(last+1)
        self.InsertCard2ListUI(first, card)

    def DeleteSelectedCards(self):
        chapter = self.ChaptersChoice.GetStringSelection()
        index = self.CardListCtrl.GetFirstSelected()
        
        while index != -1:
            self.CardListCtrl.DeleteItem(index)
            self.CardSet.DeleteCard(chapter, index)
            index = self.CardListCtrl.GetNextSelected(index-1)

        self.CardEditIndex = -1

    def MoveSelectedCards(self, NewChapter):
        chapter = self.ChaptersChoice.GetStringSelection()
        index = self.CardListCtrl.GetFirstSelected()
        
        while index != -1:
            self.CardListCtrl.DeleteItem(index)
            self.CardSet.MoveCard(chapter, index, NewChapter)
            index = self.CardListCtrl.GetNextSelected(index-1)

        self.ResetCardUI()
        self.CardEditIndex = -1

    def FindNext(self, searchStr, case=False):
        if searchStr == '':
            return

        self.FindMessage.SetLabel("")
        # Check if we are starting a new search or looking for next occurence
        if self.lastSearchStr != searchStr:
            # new search
            self.lastSearchStr = searchStr
            searchChapter = self.ChaptersChoice.GetStringSelection()
            i = self.CardSet.FindFirstStr(searchChapter, searchStr, case)
            if i < 0:
                self.FindMessage.SetLabel("Phrase not found")
        else:
            # looking for next item
            if self.searchCardIndex < 0:
                self.FindMessage.SetLabel("Phrase not found")
                i = -1
            else:
                self.lastSearchStr = searchStr
                searchChapter = self.ChaptersChoice.GetStringSelection()
                i = self.CardSet.FindNextStr(searchChapter, self.searchCardIndex, searchStr, case)
                if i < 0:
                    self.FindMessage.SetLabel("Searching from top")
                    i = self.CardSet.FindFirstStr(searchChapter, searchStr)

        self.searchCardIndex = i
        if i < 0:
            return

        # Update gui
        #
        # first deselect any cards if selected
        n = self.CardListCtrl.GetFirstSelected()
        if n >= 0:
            self.CardListCtrl.SetItemState(n, 0, wx.LIST_STATE_SELECTED)
            print "Deselecting item"
        while n >= 0:
            n = self.CardListCtrl.GetNextSelected(n)
            if n >= 0:
                self.CardListCtrl.SetItemState(n, 0, wx.LIST_STATE_SELECTED)


        # Select the card containg the search string
        self.CardListCtrl.SetItemState(self.searchCardIndex, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)

        # Bring focus back to the search ctrl
        self.SearchCtrl.SetFocus()

    def FindPrev(self, searchStr, case=False):
        if searchStr == '':
            return

        self.FindMessage.SetLabel("")

        # looking for next item
        if self.searchCardIndex < 0:
            self.FindMessage.SetLabel("Phrase not found")
            i = -1
        else:
            self.lastSearchStr = searchStr
            searchChapter = self.ChaptersChoice.GetStringSelection()
            i = self.CardSet.FindNextStr(searchChapter, self.searchCardIndex, searchStr, case, -1)
            if i < 0:
                self.FindMessage.SetLabel("Searching from bottom")
                i = self.CardSet.FindLastStr(searchChapter, searchStr)

        self.searchCardIndex = i
        if i < 0:
            return

        # Update gui
        #
        # first deselect any cards if selected
        n = self.CardListCtrl.GetFirstSelected()
        if n >= 0:
            self.CardListCtrl.SetItemState(n, 0, wx.LIST_STATE_SELECTED)
        while n >= 0:
            n = self.CardListCtrl.GetNextSelected(n)
            if n >= 0:
                self.CardListCtrl.SetItemState(n, 0, wx.LIST_STATE_SELECTED)


        # Select the card containg the search string
        self.CardListCtrl.SetItemState(self.searchCardIndex, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)

        # Bring focus back to the search ctrl
        self.SearchCtrl.SetFocus()

    def OnKeyDown(self, event):
        keycode = event.GetKeyCode()

        if event.ControlDown() and not event.ShiftDown() \
                and not event.AltDown():
            if keycode == ord('F'):
                self.SearchCtrl.SetFocus()
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

    def OnAutoCorr(self, event):
        dlg = AutoCorrDlg.AutoCorrDlg(self, -1, self.autocorr)
        dlg.ShowModal()

        self.autocorr = dlg.GetData()
        dlg.Destroy()

    def OnChaptersChoiceChoice(self, event):
        chapter = event.GetString()
        self.CardListCtrl.DeleteAllItems()
        self.AddCards2ListUI(self.CardSet.GetChapterCards(chapter))
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
            self.popupIDInsertAbove = wx.NewId()
            self.popupIDInsertBelow = wx.NewId()
            self.popupIDDelete = wx.NewId()
            self.popupIDMove = wx.NewId()
            self.popupIDChapters = [wx.NewId() for n in range(MaxPopupChapters)]

            self.Bind(wx.EVT_MENU, self.OnPopupInsertAbove, id=self.popupIDInsertAbove)
            self.Bind(wx.EVT_MENU, self.OnPopupInsertBelow, id=self.popupIDInsertBelow)
            self.Bind(wx.EVT_MENU, self.OnPopupDelete, id=self.popupIDDelete)
            self.Bind(wx.EVT_MENU, self.OnPopupMove, id=self.popupIDMove)
            for id in self.popupIDChapters:
                self.Bind(wx.EVT_MENU, self. OnPopupMoveChapter, id=id)

        # make a menu
        menu = wx.Menu()
        # add some items
        menu.Append(self.popupIDInsertAbove, "Insert Above")
        menu.Append(self.popupIDInsertBelow, "Insert Below")
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

    def OnPopupInsertAbove(self, event):
        self.InsertNewCardAbove()
        self.ResetCardUI()

    def OnPopupInsertBelow(self, event):
        self.InsertNewCardBelow()
        self.ResetCardUI()

    def OnPopupDelete(self, event):
        self.DeleteSelectedCards()
        self.ResetCardUI()

    def OnPopupMove(self, event):
        event.Skip()

    def OnPopupMoveChapter(self, event):
        chapter = self.PopupIDChapterMap[event.GetId()]
        self.MoveSelectedCards(chapter)

    def OnCardsUp(self, event):
        self.CardsUp()

    def OnCardsDown(self, event):
        self.CardsDown()

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
            if self.Config:
                w, h = self.GetSize()
                self.Config.set('card_browser', 'width', `w`)
                self.Config.set('card_browser', 'height', `h`)
            event.Skip()

    def OnFindNext(self, event):
        self.FindNext(self.SearchCtrl.GetValue())

    def OnFindPrev(self, event):
        self.FindPrev(self.SearchCtrl.GetValue())

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
