import wx
import os
from AboutDlg import AboutDlg

class TestApp(wx.App):
    def OnInit(self):
        # Get the current working directory
        runtimepath = os.getcwd()

        # Create the main window
        frame = wx.Frame(None, -1, 'Test')

        # Create an instance of the About Dialog with runtimepath
        dlg = AboutDlg(frame, runtimepath)

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
