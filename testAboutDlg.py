import wx
from AboutDlg import AboutDlg

class TestApp(wx.App):
    def OnInit(self):
        # Create the main window
        frame = wx.Frame(None, -1, 'Test')

        # Create an instance of the About Dialog
        dlg = AboutDlg(frame)

        # Show the dialog
        dlg.ShowModal()
        dlg.Destroy()

        # Close the main window
        frame.Destroy()

        return True

if __name__ == '__main__':
    # Initialize and start the application
    app = TestApp(redirect=False)
    app.MainLoop()
