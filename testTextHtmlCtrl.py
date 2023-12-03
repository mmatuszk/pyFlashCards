import sys, os
import wx

import FlashCard  # Assuming this module is available in your environment
import AutoCorr
import TextHtmlCtrl

class TestFrame(wx.Frame):
    def __init__(self, parent, id, autocorr):
        wx.Frame.__init__(self, parent, id, "Test TextHtmlCtrl", size=(400, 300))

        sizer = wx.BoxSizer(wx.VERTICAL)

        # Create a TextHtmlCtrl instance
        thc = TextHtmlCtrl.TextHtmlCtrl(self, -1, autocorr, style=wx.TE_MULTILINE)

        # Add TextHtmlCtrl to the sizer
        sizer.Add(thc, 1, wx.EXPAND)

        # Set the sizer for the frame
        self.SetSizer(sizer)

# Get the current working directory
runtimepath = os.getcwd()
print(runtimepath)

# Load the autocorr.xml from the 'test/' directory within the runtime path
filename = os.path.join(runtimepath, 'test', 'autocorr.xml')

# Initialize AutoCorr
ac = AutoCorr.AutoCorr()
ac.Load(filename)

# Create an instance of wx.App
app = wx.App(False)  # 'False' to not redirect stdout/stderr to a window

# Create and show the TestFrame
win = TestFrame(None, -1, ac)
win.Show()

# Start the application's main loop
app.MainLoop()

# Save AutoCorr data
ac.Save(filename)
