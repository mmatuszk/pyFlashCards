#-------------------------------------------------------------------------------
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
# CVS information
# $Source: /cvsroot/pyflashcards/pyFlashCards/test/test.py,v $
# $Revision: 1.1 $
# $Date: 2008/10/04 22:30:25 $
# $Author: marcin $
#-------------------------------------------------------------------------------
import wx
import ViewDlg

app=wx.PySimpleApp()
dlg=ViewDlg.ViewDialog(None, -1, "View Answer")
dlg.Maximize()
dlg.ShowModal()
#frm=ViewDlg.ViewFrame(None, -1, "View Answer")
#frm.Show()
app.MainLoop()
