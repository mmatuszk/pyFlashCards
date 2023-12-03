# testViewDlg.py
import wx
from ViewDlg import ViewDialog

class TestApp(wx.App):
    def OnInit(self):
        # self.frame = wx.Frame(None, -1, "Test View Dialog")
        # self.frame.Show()

        # Create a ViewDialog
        dlg = ViewDialog(None, -1, "View Dialog", size=(800, 600))
        sample_html_content = "<h1>Hello World</h1><p>This is a test of the ViewDialog.</p>"
        dlg.SetPage(sample_html_content)

        # Show the dialog
        dlg.ShowModal()
        dlg.Destroy()
        return True

if __name__ == '__main__':
    app = TestApp()
    app.MainLoop()
