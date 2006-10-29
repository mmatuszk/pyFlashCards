#Boa:Dialog:CardManagerDlg

import wx
import wx.lib.imagebrowser as ib

import FlashCard
import shutil, os

MaxPopupChapters = 100

def create(parent):
    return CardManagerDlg(parent)

[wxID_CARDMANAGERDLG, wxID_CARDMANAGERDLGBACKENTRY, 
 wxID_CARDMANAGERDLGBACKIMAGEBUTTON, wxID_CARDMANAGERDLGCARDCOUNT, 
 wxID_CARDMANAGERDLGCARDDOWNBTN, wxID_CARDMANAGERDLGCARDLISTCTRL, 
 wxID_CARDMANAGERDLGCARDUPBTN, wxID_CARDMANAGERDLGCHAPTERSCHOICE, 
 wxID_CARDMANAGERDLGCOMMITCARDBTN, wxID_CARDMANAGERDLGDELETECARDBTN, 
 wxID_CARDMANAGERDLGFINDNEXTBTN, wxID_CARDMANAGERDLGFINDPREVIOUSBTN, 
 wxID_CARDMANAGERDLGFINDTEXTCTRL, wxID_CARDMANAGERDLGFRONTENTRY, 
 wxID_CARDMANAGERDLGFRONTIMAGEBUTTON, 
 wxID_CARDMANAGERDLGREMOVEBACKIMAGEBUTTON, 
 wxID_CARDMANAGERDLGREMOVEFRONTIMAGEBUTTON, wxID_CARDMANAGERDLGSTATICTEXT1, 
 wxID_CARDMANAGERDLGSTATICTEXT2, wxID_CARDMANAGERDLGSTATICTEXT3, 
 wxID_CARDMANAGERDLGSTATICTEXT4, wxID_CARDMANAGERDLGSTATICTEXT5, 
] = [wx.NewId() for _init_ctrls in range(22)]

class CardManagerDlg(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_CARDMANAGERDLG, name=u'CardManagerDlg',
              parent=prnt, pos=wx.Point(7, 84), size=wx.Size(1248, 750),
              style=wx.TAB_TRAVERSAL | wx.DEFAULT_DIALOG_STYLE,
              title=u'Card Manager')
        self.SetClientSize(wx.Size(1240, 707))

        self.FrontEntry = wx.TextCtrl(id=wxID_CARDMANAGERDLGFRONTENTRY,
              name=u'FrontEntry', parent=self, pos=wx.Point(72, 56),
              size=wx.Size(576, 250), style=wx.TE_MULTILINE | wx.TE_RICH2,
              value=u'')

        self.BackEntry = wx.TextCtrl(id=wxID_CARDMANAGERDLGBACKENTRY,
              name=u'BackEntry', parent=self, pos=wx.Point(72, 328),
              size=wx.Size(576, 250), style=wx.TE_MULTILINE | wx.TE_RICH2,
              value=u'')

        self.CommitCardBtn = wx.Button(id=wxID_CARDMANAGERDLGCOMMITCARDBTN,
              label=u'Commit Card', name=u'CommitCardBtn', parent=self,
              pos=wx.Point(216, 592), size=wx.Size(75, 23), style=0)
        self.CommitCardBtn.Bind(wx.EVT_BUTTON, self.OnCommitCardBtnButton,
              id=wxID_CARDMANAGERDLGCOMMITCARDBTN)

        self.DeleteCardBtn = wx.Button(id=wxID_CARDMANAGERDLGDELETECARDBTN,
              label=u'Cancel Changes', name=u'DeleteCardBtn', parent=self,
              pos=wx.Point(312, 592), size=wx.Size(96, 23), style=0)
        self.DeleteCardBtn.Bind(wx.EVT_BUTTON, self.OnCancelChangesButton,
              id=wxID_CARDMANAGERDLGDELETECARDBTN)

        self.staticText1 = wx.StaticText(id=wxID_CARDMANAGERDLGSTATICTEXT1,
              label=u'Front', name='staticText1', parent=self, pos=wx.Point(16,
              56), size=wx.Size(30, 13), style=0)

        self.staticText2 = wx.StaticText(id=wxID_CARDMANAGERDLGSTATICTEXT2,
              label=u'Chapter', name='staticText2', parent=self,
              pos=wx.Point(16, 16), size=wx.Size(50, 13), style=0)

        self.staticText3 = wx.StaticText(id=wxID_CARDMANAGERDLGSTATICTEXT3,
              label=u'Back', name='staticText3', parent=self, pos=wx.Point(16,
              328), size=wx.Size(30, 13), style=0)

        self.staticText4 = wx.StaticText(id=wxID_CARDMANAGERDLGSTATICTEXT4,
              label=u'Find Card', name='staticText4', parent=self,
              pos=wx.Point(16, 656), size=wx.Size(50, 13), style=0)

        self.FindTextCtrl = wx.TextCtrl(id=wxID_CARDMANAGERDLGFINDTEXTCTRL,
              name=u'FindTextCtrl', parent=self, pos=wx.Point(72, 652),
              size=wx.Size(184, 21), style=0, value=u'')

        self.FindNextBtn = wx.Button(id=wxID_CARDMANAGERDLGFINDNEXTBTN,
              label=u'Find Next', name=u'FindNextBtn', parent=self,
              pos=wx.Point(296, 651), size=wx.Size(75, 23), style=0)
        self.FindNextBtn.Bind(wx.EVT_BUTTON, self.OnFindNextBtnButton,
              id=wxID_CARDMANAGERDLGFINDNEXTBTN)

        self.FindPreviousBtn = wx.Button(id=wxID_CARDMANAGERDLGFINDPREVIOUSBTN,
              label=u'FindPrevious', name=u'FindPreviousBtn', parent=self,
              pos=wx.Point(392, 651), size=wx.Size(75, 23), style=0)
        self.FindPreviousBtn.Bind(wx.EVT_BUTTON, self.OnFindPreviousBtnButton,
              id=wxID_CARDMANAGERDLGFINDPREVIOUSBTN)

        self.CardListCtrl = wx.ListCtrl(id=wxID_CARDMANAGERDLGCARDLISTCTRL,
              name=u'CardListCtrl', parent=self, pos=wx.Point(816, 56),
              size=wx.Size(312, 624), style=wx.LC_REPORT)
        self.CardListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED,
              self.OnCardListCtrlListItemSelected,
              id=wxID_CARDMANAGERDLGCARDLISTCTRL)
        self.CardListCtrl.Bind(wx.EVT_LIST_ITEM_DESELECTED,
              self.OnCardListCtrlListItemDeselected,
              id=wxID_CARDMANAGERDLGCARDLISTCTRL)
        self.CardListCtrl.Bind(wx.EVT_CHAR, self.OnCardListCtrlChar)

        self.CardUpBtn = wx.Button(id=wxID_CARDMANAGERDLGCARDUPBTN, label=u'Up',
              name=u'CardUpBtn', parent=self, pos=wx.Point(1152, 296),
              size=wx.Size(75, 23), style=0)

        self.CardDownBtn = wx.Button(id=wxID_CARDMANAGERDLGCARDDOWNBTN,
              label=u'Down', name=u'CardDownBtn', parent=self,
              pos=wx.Point(1152, 328), size=wx.Size(75, 23), style=0)

        self.staticText5 = wx.StaticText(id=wxID_CARDMANAGERDLGSTATICTEXT5,
              label=u'Cards', name='staticText5', parent=self, pos=wx.Point(816,
              16), size=wx.Size(35, 13), style=0)

        self.ChaptersChoice = wx.Choice(choices=[],
              id=wxID_CARDMANAGERDLGCHAPTERSCHOICE, name=u'ChaptersChoice',
              parent=self, pos=wx.Point(72, 16), size=wx.Size(400, 24),
              style=0)
        self.ChaptersChoice.Bind(wx.EVT_CHOICE, self.OnChaptersChoiceChoice,
              id=wxID_CARDMANAGERDLGCHAPTERSCHOICE)

        self.FrontImageButton = wx.BitmapButton(bitmap=wx.NullBitmap,
              id=wxID_CARDMANAGERDLGFRONTIMAGEBUTTON, name=u'FrontImageButton',
              parent=self, pos=wx.Point(672, 81), size=wx.Size(120, 120),
              style=wx.BU_AUTODRAW)
        self.FrontImageButton.Bind(wx.EVT_BUTTON, self.OnFrontImageButtonButton,
              id=wxID_CARDMANAGERDLGFRONTIMAGEBUTTON)

        self.BackImageButton = wx.BitmapButton(bitmap=wx.NullBitmap,
              id=wxID_CARDMANAGERDLGBACKIMAGEBUTTON, name=u'BackImageButton',
              parent=self, pos=wx.Point(672, 361), size=wx.Size(120, 120),
              style=wx.BU_AUTODRAW)
        self.BackImageButton.Bind(wx.EVT_BUTTON, self.OnBackImageButtonButton,
              id=wxID_CARDMANAGERDLGBACKIMAGEBUTTON)

        self.RemoveFrontImageButton = wx.Button(id=wxID_CARDMANAGERDLGREMOVEFRONTIMAGEBUTTON,
              label=u'Remove Image', name=u'RemoveFrontImageButton',
              parent=self, pos=wx.Point(688, 218), size=wx.Size(88, 23),
              style=0)
        self.RemoveFrontImageButton.Bind(wx.EVT_BUTTON,
              self.OnRemoveFrontImageButtonButton,
              id=wxID_CARDMANAGERDLGREMOVEFRONTIMAGEBUTTON)

        self.RemoveBackImageButton = wx.Button(id=wxID_CARDMANAGERDLGREMOVEBACKIMAGEBUTTON,
              label=u'Remove Image', name=u'RemoveBackImageButton', parent=self,
              pos=wx.Point(688, 498), size=wx.Size(88, 23), style=0)
        self.RemoveBackImageButton.Bind(wx.EVT_BUTTON,
              self.OnRemoveBackImageButtonButton,
              id=wxID_CARDMANAGERDLGREMOVEBACKIMAGEBUTTON)

        self.CardCount = wx.TextCtrl(id=wxID_CARDMANAGERDLGCARDCOUNT,
              name=u'CardCount', parent=self, pos=wx.Point(872, 12),
              size=wx.Size(48, 21), style=wx.TE_READONLY, value=u'')

    def __init__(self, parent, CardSet, Config):
        # Call the boa generate function to initialize controls
        self._init_ctrls(parent)

        # Adjust the size of some buttons
        self.CommitCardBtn.SetBestFittingSize()
        self.DeleteCardBtn.SetBestFittingSize()
        self.FindNextBtn.SetBestFittingSize()
        self.FindPreviousBtn.SetBestFittingSize()
        self.RemoveFrontImageButton.SetBestFittingSize()
        self.RemoveBackImageButton.SetBestFittingSize()

        # Adjust the size of the chapter choice
        bw, bh = self.ChaptersChoice.GetBestSize()
        w, h = self.ChaptersChoice.GetSize()
        size = (w, bh)
        self.ChaptersChoice.SetSize(size)
        
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

    def SelectCard(self, card):
        chapter = card.GetChapter()

        # Select chapter 
        self.ChaptersChoice.SetStringSelection(chapter)
        self.CardListCtrl.DeleteAllItems()
        self.AddCards2List(self.CardSet.GetChapterCards(chapter))

        # Select card for edit
        index = self.CardSet.GetCardIndex(card)
        self.CardListCtrl.SetItemState(index, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)

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

        self.NoImageBitmap = wx.Image('icons/noimage.jpg', wx.BITMAP_TYPE_JPEG).ConvertToBitmap()
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
            self.FrontImageButton.SetBitmapLabel(MakeButtonBitmap(self.FrontImage, bsize))
        else:
            self.FrontImageButton.SetBitmapLabel(self.NoImageBitmap)

        if self.BackImage:
            bsize = self.BackImageButton.GetSize()
            self.BackImageButton.SetBitmapLabel(MakeButtonBitmap(self.BackImage, bsize))
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
                        # If yes, we need to remove the old image and set the new one
                        os.remove(self.FrontImage)
                        card.SetFrontImage(self.MakeCardImage(self.NewFrontImage))
                    else:
                        # We need to remove the image
                        os.remove(self.FrontImage)
                        card.SetFrontImage(None)
                else:
                    # There was no image to begin with
                    if self.NewFrontImage:
                        # Create a new image
                        card.SetFrontImage(self.MakeCardImage(self.NewFrontImage))
                    else:
                        # Nothing to do, an image was probably added and then removed
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
                        # If yes, we need to remove the old image and set the new one
                        os.remove(self.BackImage)
                        card.SetBackImage(self.MakeCardImage(self.NewBackImage))
                    else:
                        # We need to remove the image
                        os.remove(self.BackImage)
                        card.SetBackImage(None)
                else:
                    # There was no image to begin with
                    if self.NewBackImage:
                        # Create a new image
                        card.SetBackImage(self.MakeCardImage(self.NewBackImage))
                    else:
                        # Nothing to do, an image was probably added and then removed
                        pass
            else:
                # If the image did not change, there is no need to do anything
                pass

            # Update GUI controls
            self.CardListCtrl.SetStringItem(index, 0, card.GetFrontText())
            self.CardListCtrl.SetStringItem(index, 1, card.GetBackText())
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

    def OnCancelChangesButton(self, event):
        index = self.CardEditIndex
        if index >= 0:
            self.CardListCtrl.SetItemState(index, 0, wx.LIST_STATE_SELECTED)

        self.CancelCardEdit()
        self.FrontEntry.SetFocus()
        
        self.CardEditIndex = -1

    def OnFindNextBtnButton(self, event):
        event.Skip()

    def OnFindPreviousBtnButton(self, event):
        event.Skip()

    def OnChaptersChoiceChoice(self, event):
        chapter = event.GetString()
        self.CardListCtrl.DeleteAllItems()
        self.AddCards2List(self.CardSet.GetChapterCards(chapter))
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
            self.UpdateCardCountUI()
        else:
            event.Skip()

    def OnFrontImageButtonButton(self, event):
        dir = self.Config.get('directories', 'image_dir')
        dlg = ib.ImageDialog(self, dir)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetFile()
            
            # Update config
            self.Config.set('directories', 'image_dir', os.path.dirname(filename))

            self.NewFrontImage = filename
            self.FrontImageChanged = True

            # Create the bitmap for the button
            bsize = self.FrontImageButton.GetSize()

            self.FrontImageButton.SetBitmapLabel(MakeButtonBitmap(self.NewFrontImage, bsize))

        dlg.Destroy()

    def OnBackImageButtonButton(self, event):
        dir = self.Config.get('directories', 'image_dir')
        dlg = ib.ImageDialog(self, dir)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetFile()
            
            # Update config
            self.Config.set('directories', 'image_dir', os.path.dirname(filename))

            self.NewBackImage = filename
            self.BackImageChanged = True

            # Create the bitmap for the button
            bsize = self.BackImageButton.GetSize()

            self.BackImageButton.SetBitmapLabel(MakeButtonBitmap(self.NewBackImage, bsize))

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
        for chapter, id in zip(self.CardSet.GetChapters(), self.popupIDChapters):
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
        self.UpdateCardCountUI()

    def OnPopupMove(self, event):
        event.Skip()

    def OnPopupMoveChapter(self, event):
        chapter = self.PopupIDChapterMap[event.GetId()]
        self.MoveSelectedCards(chapter)

def MakeButtonBitmap(filename, bsize, pad=10):
        bw, bh = bsize
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
