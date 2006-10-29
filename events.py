import wx

myEVT_WINDOW_CLOSED = wx.NewEventType()
EVT_WINDOW_CLOSED   = wx.PyEventBinder(myEVT_WINDOW_CLOSED, 1)

class WindowClosedEvent(wx.PyCommandEvent):
    def __init__(self, evtType, id):
        wx.PyCommandEvent.__init__(self, evtType, id)

