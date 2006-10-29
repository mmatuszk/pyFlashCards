import wx

import FlashCard

ID_BOX_MANAGER_DLG = wx.NewId()

ID_BM_BOX_MAX_TEXT = [wx.NewId() for x in range(FlashCard.BoxNum)]

class BoxManagerDlg(wx.Dialog):
    def __init__(self, parent, CardSet):
        wx.Dialog.__init__(self, parent, ID_BOX_MANAGER_DLG, 'Box manager dialog')

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.nb = BoxManagerNB(self, -1, CardSet)
        sizer.Add(self.nb, 0, wx.ALL, 20)

        sizer1 = wx.BoxSizer(wx.HORIZONTAL)

        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        sizer1.Add(btn)
        btn = wx.Button(self, wx.ID_CANCEL)
        sizer1.Add(btn)

        sizer.Add(sizer1, 0, wx.ALIGN_RIGHT | wx.ALL, 20)
        
        self.SetAutoLayout(True)
        self.SetSizerAndFit(sizer)

    def GetData(self):
        return self.nb.GetData()

class BoxManagerNB(wx.Notebook):
    def __init__(self, parent, id, CardSet):
        wx.Notebook.__init__(self, parent, id, #size=(200,200),
                             #style=
                             #wx.NB_TOP # | wx.NB_MULTILINE
                             #wx.NB_BOTTOM
                             #wx.NB_LEFT
                             #wx.NB_RIGHT
                             )

        self.p1 = BoxSizePanel(self, -1, CardSet)
        self.AddPage(self.p1, 'Box Sizes')

        self.p2 = LearnBoxesPanel(self, -1, CardSet)
        self.AddPage(self.p2, 'Learn Boxes ...')

    def GetData(self):
        return self.p1.GetData(), self.p2.GetData()

class BoxSizePanel(wx.Panel):
    def __init__(self, parent, id, CardSet):
        wx.Panel.__init__(self, parent, id)

        # First create a count control and determine all sizes from it
        count = wx.TextCtrl(self, -1, style = wx.TE_READONLY)
        w = count.GetFont().GetPointSize()
        TextSize = count.GetSize()
        # Change width to 4 characters
        TextSize[0] = w*5
        count.SetBestFittingSize(TextSize)

        # Set the size of the gauge control based on the size of the text control
        GaugeSize = (200, TextSize[1])

        sizer = wx.GridBagSizer(5, 11)

        # Create remaining pool controls 
        label = wx.StaticText(self, -1, 'Pool')
        gauge = wx.Gauge(self, -1, size = GaugeSize, range=100, style = wx.GA_HORIZONTAL | wx.GA_SMOOTH)
        lsep = wx.StaticText(self, -1, '/')
        max = wx.TextCtrl(self, -1, size = TextSize, style = wx.TE_READONLY)

        c = CardSet.GetBoxCardCount(0)
        count.SetValue(`c`)
        m = CardSet.GetTestCardsCount()
        max.SetValue(`m`)
        if m == 0:
            gauge.SetValue(0)
        else:
            gauge.SetValue(100*c/m)

        # Add all pool controls to the sizer
        sizer.Add(label, (0, 0))
        sizer.Add(gauge, (0, 1))
        sizer.Add(count, (0, 2))
        sizer.Add(lsep, (0, 3))
        sizer.Add(max, (0, 4))

        self.MaxMap = {}
        self.MaxCtrlList = []
        # Create controls for all the boxes remaining boxes.  The pool controls are already done.
        for n in range(0, FlashCard.BoxNum):
            label = wx.StaticText(self, -1, 'Box %d' % (n+1))
            gauge = wx.Gauge(self, -1, size = GaugeSize, range=100, style = wx.GA_HORIZONTAL | wx.GA_SMOOTH)
            count = wx.TextCtrl(self, -1, size = TextSize, style = wx.TE_READONLY)
            lsep = wx.StaticText(self, -1, '/')
            max = wx.TextCtrl(self, ID_BM_BOX_MAX_TEXT[n], size = TextSize)#, style = wx.TE_PROCESS_ENTER)

            # This list contains tuplet of (box number, max items control)
            self.MaxCtrlList.append((n+1, max))
            
            c = CardSet.GetBoxCardCount(n+1)
            count.SetValue(`c`)
            m =  CardSet.GetBoxCapacity(n+1)
            max.SetValue(`m`)
            gauge.SetValue(100*c/m)

            sizer.Add(label, (n+1, 0))
            sizer.Add(gauge, (n+1, 1))
            sizer.Add(count, (n+1, 2))
            sizer.Add(lsep, (n+1, 3))
            sizer.Add(max, (n+1, 4))


        self.SetSizerAndFit(sizer)

        label.SetFocus() 

    #---------------------------------------------------------------------------
    # Return a list of all maximum item counts.  If the user entered a new
    # value which is not an integer it will be returned as such and needs to 
    # be handaled in the calling function.
    #
    # The format of the returned value is a list of tuplets
    # (box index, max capacity)
    #---------------------------------------------------------------------------
    def GetData(self):
        l = []
        for i, ctrl in self.MaxCtrlList:
            l.append((i, ctrl.GetValue()))

        return l

class LearnBoxesPanel(wx.Panel):
    def __init__(self, parent, id, CardSet):
        wx.Panel.__init__(self, parent, id)

        sizer = wx.BoxSizer(wx.VERTICAL)

        # Create a control for all boxes
        list = ['All boxes']
        for n in range(0, FlashCard.BoxNum):
            list.append('Box %d' % (n+1))

        self.rb = wx.RadioBox(
                self, -1, "Choose which box to learn", wx.DefaultPosition, wx.DefaultSize,
                list, 1, wx.RA_SPECIFY_COLS
                )

        for n in range(0, FlashCard.BoxNum):
            if CardSet.GetBoxCardCount(n+1) == 0:
                self.rb.EnableItem(n+1, False)

        box = CardSet.GetStudyBox()
        self.rb.SetSelection(box)

        sizer.Add(self.rb, 0, wx.ALL, 20)

        self.SetSizerAndFit(sizer)
    #---------------------------------------------------------------------------
    # Return the number of the box to learn from
    # 0 - all boxes
    # 1 - box 1
    # 2 - box 2
    # ...
    # 10 - box 10
    #---------------------------------------------------------------------------
    def GetData(self):
        return self.rb.GetSelection()
