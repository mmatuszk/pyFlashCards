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
            if keycode == ord('B'):
                self.Bold()
                return
            if keycode == ord ('U'):
                self.Underline()
                return
            if keycode == ord('I'):
                self.Italic()
                return
            if keycode == ord('Q'):
                self.Color('red')
                return
            if keycode == ord('W'):
                self.Color('green')
                return
            if keycode == ord('E'):
                self.Color('blue')
            if keycode is ord('-'):
                self.Subscript()
            if keycode is ord('='):
                self.Superscript()
                return
            if keycode == ord('L'):
                self.InsertLeftArrow()
                return
            if keycode == ord('P'):
                self.InsertUpArrow()
                return
            if keycode == ord('R'):
                self.InsertRightArrow()
                return
            if keycode == ord('D'):
                self.InsertDownArrow()
                return

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

    def Subscript(self):
        s_tag = '<sub>'
        e_tag = '</sub>'

        self.InsertTag(s_tag, e_tag)

    def Superscript(self):
        s_tag = '<sup>'
        e_tag = '</sup>'

        self.InsertTag(s_tag, e_tag)

    # Insert a string
    # Replace a any selected string
    def InsertString(self, string):
        s,e = self.GetSelection()

        self.Replace(s, e, string)
        return

    def InsertLeftArrow(self):
        self.InsertString(u'\u2190')

    def InsertUpArrow(self):
        self.InsertString(u'\u2191')

    def InsertRightArrow(self):
        self.InsertString(u'\u2192')

    def InsertDownArrow(self):
        self.InsertString(u'\u2193')

