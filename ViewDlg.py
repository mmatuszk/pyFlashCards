#-------------------------------------------------------------------------------
# ViewDlg.py
# Dialog made for viewing the answer in full screen
#
# Author:   Marcin Matuszkiewicz
#-------------------------------------------------------------------------------
# pyFlashCards is a multiplatform flash cards software.
# Copyright (C) 2006  Marcin Matuszkiewicz
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
#   Foundation, Inc.
#   51 Franklin Street, Fifth Floor
#   Boston
#   MA  02110-1301
#   USA.
#-------------------------------------------------------------------------------

import wx
import wx.html as html

class ViewDialog(wx.Dialog):
    def __init__(
            self, parent, ID, title, size=wx.DefaultSize, pos=wx.DefaultPosition, 
            style=wx.DEFAULT_DIALOG_STYLE | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER
            ):
        # Directly create the dialog
        super(ViewDialog, self).__init__(parent, ID, title, pos, size, style)

        # Now continue with the normal construction of the dialog contents
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.html = html.HtmlWindow(self, -1, style=wx.SUNKEN_BORDER | wx.HSCROLL)

        sizer.Add(self.html, 1, wx.EXPAND)

        self.SetSizer(sizer)
        sizer.Fit(self)

         # Maximize the dialog
        self.Maximize(True)

    def SetPage(self, page):
        self.html.SetPage(page)
