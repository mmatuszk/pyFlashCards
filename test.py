import wx
import ViewDlg

app=wx.PySimpleApp()
dlg=ViewDlg.ViewDialog(None, -1, "View Answer")
dlg.Maximize()
dlg.ShowModal()
#frm=ViewDlg.ViewFrame(None, -1, "View Answer")
#frm.Show()
app.MainLoop()
