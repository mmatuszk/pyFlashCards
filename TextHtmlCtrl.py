# TextHtmlCtrl.py
import wx
import platform

# Determine the operating system
is_windows = platform.system() == 'Windows'

def print_index_and_char(text):
    result = {index: char for index, char in enumerate(text)}
    print(result)

# TextHtmlCtrl
#
# A specialized wx.TextCtrl for HTML content editing in wxPython applications.
# This class extends the functionality of the standard wx.TextCtrl to include
# features tailored for convenient HTML editing. It incorporates auto-correction
# capabilities, enabling the automatic replacement of common typing errors with
# the correct text. Additionally, this control offers a range of keyboard shortcuts
# for quickly inserting standard HTML tags and special characters, enhancing
# the efficiency of HTML content creation and formatting.
#
# The control binds to specific keyboard events to implement its functionality.
# The OnKeyDown event is used for detecting and responding to keyboard shortcuts,
# while the OnText event manages the auto-correction feature. This control makes
# HTML editing more accessible and user-friendly within wxPython applications,
# particularly for users who frequently work with HTML content.

class TextHtmlCtrl(wx.TextCtrl):
    def __init__(self, parent, id, autocorr, value="", pos=wx.DefaultPosition,
            size=wx.DefaultSize, style=0, validator=wx.DefaultValidator,
            name=wx.TextCtrlNameStr):

        self.autocorr = autocorr

        wx.TextCtrl.__init__(self, parent, id, value, pos, size, style,
                             validator, name)

        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.Bind(wx.EVT_TEXT, self.OnText)


    # def OnText(self, event):
    #     text = self.GetValue()
    #     if len(text) == 0:
    #         return

    #     end = self.GetInsertionPoint() - 1

    #     # Ensure 'end' is within the bounds of the text
    #     if end >= len(text):
    #         return

    #     # Adjust for different newline representations
    #     if is_windows:
    #         # Windows specific logic (\r\n)
    #         if end >= 1 and text[end] == '\n' and text[end-1] == '\r':
    #             end -= 2
    #     else:
    #         # Unix-like systems (\n)
    #         if end >= 0 and text[end] == '\n':
    #             end -= 1

    #     if end < 0:
    #         return

    #     start = end - 1
    #     while start >= 0 and not text[start].isspace():
    #         start -= 1

    #     if start < 0 or text[start].isspace():
    #         start += 1
    #         newText = self.autocorr.FindReplace(text[start:end+1])
    #         if newText != text[start:end+1]:
    #             self.Replace(start, end+1, newText)

    #     event.Skip()
    def OnText(self, event):
        if is_windows:
            text = self.GetValue()
            text = text.replace('\n', '\r\n')  # Replace '\n' with '\r\n' for Windows

            if len(text) == 0:
                return

            end = self.GetInsertionPoint()-1

            # Adjust for Windows-style newlines if at the end of a line
            if end > 0 and text[end - 1] == '\n':
                end -= 1

            start = end-1
            if text[end].isspace():
                while start >= 0 and not text[start].isspace():
                    start -= 1

                if start < 0 or text[start].isspace():
                    start += 1
                    #print text[start:end+1]
                    newText = self.autocorr.FindReplace(text[start:end+1])
                    if newText != text[start:end+1]:
                        self.Replace(start, end+1, newText)
        else:
            text = self.GetValue()
            if len(text) == 0:
                return

            len_text = len(text)
            end = self.GetInsertionPoint()-1
            start = end-1

            if text[end].isspace():
                while start >= 0 and not text[start].isspace():
                    start -= 1

                if start < 0 or text[start].isspace():
                    start += 1
                    #print text[start:end+1]
                    newText = self.autocorr.FindReplace(text[start:end+1])
                    if newText != text[start:end+1]:
                        self.Replace(start, end+1, newText)

        event.Skip()

    def OnKeyDown(self, event):
        keycode = event.GetKeyCode()

        if event.ControlDown() and not event.ShiftDown() \
                and not event.AltDown():
            if keycode == ord('1'):
                self.H1()
                return
            if keycode == ord('2'):
                self.H2()
                return
            if keycode == ord('3'):
                self.H3()
                return
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
                return
            if keycode == ord('M'):
                self.TableRowShort()
                return
            if keycode == ord('N'):
                self.TableDataShort()
                return
            if keycode == ord('J'):
                self.Break()
                return
            if keycode is ord('-'):
                self.Subscript()
                return
            if keycode is ord('+'):
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
            if keycode == ord('K'):
                self.InsertWarning()
                return
            if keycode == ord('0'):
                self.InsertDegree()
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

    def H1(self):
        s_tag = '<h1>'
        e_tag = '</h1>'

        self.InsertTag(s_tag, e_tag)
    def H2(self):
        s_tag = '<h2>'
        e_tag = '</h2>'

        self.InsertTag(s_tag, e_tag)
    def H3(self):
        s_tag = '<h3>'
        e_tag = '</h3>'

        self.InsertTag(s_tag, e_tag)
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

    def TableRowShort(self):
        self.InsertString('<tr>')

    def TableDataShort(self):
        self.InsertString('<td valign=top>')

    def Break(self):
        self.InsertString('<br>')

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

    def InsertWarning(self):
        self.InsertString(u'\u26A0')

    def InsertDegree(self):
        self.InsertString(u"\u00B0")
