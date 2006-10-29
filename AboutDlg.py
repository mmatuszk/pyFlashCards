import wx
import wx.html as html
import ver

ID_ABOUT_DLG = wx.NewId()

license_str =\
"""
<html>
<body>
<h3>Credits</h3>
Marcin Matuszkiewicz
<h3>License</h3>
This is free software.  It can be distributed under the term of the GNU General Public license.
</body>
<html>
"""

class AboutDlg(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, ID_ABOUT_DLG, 'About pyFlashCards')

        sizer = wx.BoxSizer(wx.VERTICAL)

        img = wx.Image('icons/pyFlashCards.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        logo = wx.StaticBitmap(self, -1, img)

        title = wx.StaticText(self, -1, 'pyFlashCards %d.%d.%d' % (ver.major, ver.minor, ver.build))
        f = title.GetFont()
        f.SetPointSize(18)
        title.SetFont(f)

        license = html.HtmlWindow(self, -1, size=(400, 200))
        license.SetPage(license_str)
        

        button = wx.Button(self, wx.ID_OK, 'OK')
        

        sizer.Add(logo, 0, wx.CENTER, 10)
        sizer.Add(title, 0, wx.ALL | wx.CENTER, 10)
        sizer.Add(license, 0, wx.ALL | wx.CENTER, 10)
        sizer.Add(button, 0, wx.ALL | wx.CENTER, 10)

        self.SetSizerAndFit(sizer)
