import wx

class TextHtmlCtrl(wx.TextCtrl):
    def __init__(self, parent, id, value="", pos=wx.DefaultPosition,
            size=wx.DefaultSize, style=0, validator=wx.DefaultValidator,
            name=wx.TextCtrlNameStr):

        wx.TextCtrl.__init__(self, parent, id, value, pos, size, style,
                             validator, name)

        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

    def OnKeyDown(self, event):
        keycode = event.GetKeyCode()

        if event.ControlDown() and not event.ShiftDown() \
                and not event.AltDown():
            if keycode is ord('B'):
                self.Bold()
            if keycode is ord ('U'):
                self.Underline()
            if keycode is ord('I'):
                self.Italic()
            if keycode is ord('Q'):
                self.Color('red')
            if keycode is ord('W'):
                self.Color('green')
            if keycode is ord('E'):
                self.Color('blue')

        event.Skip()

    def InsertTag(self, s_tag, e_tag):
        s,e = self.GetSelection()

        if s == e:
            self.WriteText(s_tag+e_tag)
            self.SetInsertionPoint(s+len(s_tag))
        else:
            self.SetInsertionPoint(s)
            self.WriteText(s_tag)
            self.SetInsertionPoint(e+len(s_tag))
            self.WriteText(e_tag)
            self.SetSelection(s+len(s_tag), e+len(s_tag))

    def Bold(self):
        s_tag = '<b>'
        e_tag = '</b>'

        self.InsertTag(s_tag, e_tag)

    def Italic(self):
        s_tag = '<i>'
        e_tag = '</i>'
        
        self.InsertTag(s_tag, e_tag)

    def Underline(self):
        s_tag = '<u>'
        e_tag = '</u>'

        self.InsertTag(s_tag, e_tag)


    def Color(self, color='red'):
        s_tag = '<font color=%s>' % color
        e_tag = '</font>'

        self.InsertTag(s_tag, e_tag)
