#Boa:Dialog:ChapterManagerDlg

import wx
import FlashCard

def create(parent):
    return ChapterManagerDlg(parent)

[wxID_CHAPTERMANAGERDLG, wxID_CHAPTERMANAGERDLGCHAPTERLISTCTRL, 
 wxID_CHAPTERMANAGERDLGCHAPTERTITLEENTRY, wxID_CHAPTERMANAGERDLGSTATICTEXT1, 
] = [wx.NewId() for _init_ctrls in range(4)]

class ChapterManagerDlg(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_CHAPTERMANAGERDLG,
              name=u'ChapterManagerDlg', parent=prnt, pos=wx.Point(466, 264),
              size=wx.Size(372, 383), style=wx.DEFAULT_DIALOG_STYLE,
              title=u'Chapter Manager')
        self.SetClientSize(wx.Size(364, 345))

        self.ChapterListCtrl = wx.ListCtrl(id=wxID_CHAPTERMANAGERDLGCHAPTERLISTCTRL,
              name=u'ChapterListCtrl', parent=self, pos=wx.Point(16, 16),
              size=wx.Size(328, 272), style=wx.LC_REPORT)
        self.ChapterListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED,
              self.OnChapterListCtrlListItemSelected,
              id=wxID_CHAPTERMANAGERDLGCHAPTERLISTCTRL)
        self.ChapterListCtrl.Bind(wx.EVT_LIST_ITEM_DESELECTED,
              self.OnChapterListCtrlListItemDeselected,
              id=wxID_CHAPTERMANAGERDLGCHAPTERLISTCTRL)
        self.ChapterListCtrl.Bind(wx.EVT_CHAR, self.OnChapterListCtrlChar)

        self.ChapterTitleEntry = wx.TextCtrl(id=wxID_CHAPTERMANAGERDLGCHAPTERTITLEENTRY,
              name=u'ChapterTitleEntry', parent=self, pos=wx.Point(112, 304),
              size=wx.Size(232, 21), style=wx.TE_PROCESS_ENTER, value=u'')
        self.ChapterTitleEntry.Bind(wx.EVT_TEXT_ENTER,
              self.OnChapterTitleEntryTextEnter,
              id=wxID_CHAPTERMANAGERDLGCHAPTERTITLEENTRY)
        self.ChapterTitleEntry.Bind(wx.EVT_CHAR, self.OnChapterTitleEntryChar)

        self.staticText1 = wx.StaticText(id=wxID_CHAPTERMANAGERDLGSTATICTEXT1,
              label=u'Chapter title', name='staticText1', parent=self,
              pos=wx.Point(16, 312), size=wx.Size(56, 13), style=0)

    def __init__(self, parent, CardSet):
        self._init_ctrls(parent)

        self.CardSet = CardSet
        self.ChapterEditIndex = -1
        self.OldChapterTitle = ''

        width = self.ChapterListCtrl.GetSize()[0]-4
        self.ChapterListCtrl.InsertColumn(0, "Chapter", width = width*0.2)
        self.ChapterListCtrl.InsertColumn(1, "Title", width = width*0.8)

        self.AddChapters2List(self.CardSet.GetChapters())

        self.ChapterTitleEntry.SetFocus()

    def AddChapters2List(self, list):
        for chapter in list:
            label = self.CardSet.GetChapterLabel(chapter)
            # Insert cards at the end of the list by getting the index from the
            # number of items in the list
            index = self.ChapterListCtrl.GetItemCount()
            self.ChapterListCtrl.InsertStringItem(index, label)            
            self.ChapterListCtrl.SetStringItem(index, 1, chapter)

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
            except FlashCard.FlashCardError, err:
                MsgWin = wx.MessageDialog(self, err.getValue(), 'Error', wx.OK | wx.ICON_ERROR)
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
