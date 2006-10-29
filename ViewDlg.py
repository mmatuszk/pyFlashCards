# ViewDlg.py
# Dialog made for viewing the answer in full screen

import wx
import wx.html as html

class ViewDialog(wx.Dialog):
    def __init__(
            self, parent, ID, title, size=wx.DefaultSize, pos=wx.DefaultPosition, 
            style=wx.DEFAULT_DIALOG_STYLE | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER
            ):
        # Instead of calling wx.Dialog.__init__ we precreate the dialog
        # so we can set an extra style that must be set before
        # creation, and then we create the GUI dialog using the Create
        # method.
        pre = wx.PreDialog()
        pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        pre.Create(parent, ID, title, pos, size, style)

        # This next step is the most important, it turns this Python
        # object into the real wrapper of the dialog (instead of pre)
        # as far as the wxPython extension is concerned.
        self.PostCreate(pre)

        # Now continue with the normal construction of the dialog
        # contents
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.html = html.HtmlWindow(self, -1, style=wx.SUNKEN_BORDER | wx.HSCROLL)

        sizer.Add(self.html, 1, wx.EXPAND)

        self.SetSizer(sizer)
        sizer.Fit(self)

    def SetPage(self, page):
        self.html.SetPage(page)
