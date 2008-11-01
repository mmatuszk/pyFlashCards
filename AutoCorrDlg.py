#-------------------------------------------------------------------------------
# AutoCorrDlg.py
# Dialog for editing find replace pairs
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
# CVS information
# $Source: /cvsroot/pyflashcards/pyFlashCards/AutoCorrDlg.py,v $
# $Revision: 1.2 $
# $Date: 2008/11/01 16:14:23 $
# $Author: marcin201 $
#-------------------------------------------------------------------------------

import wx

class AutoCorrDlg(wx.Dialog):
    def __init__(
            self, parent, ID, autocorr, title='AutoCorr', 
            size=(600, 500), pos=wx.DefaultPosition, 
            style=wx.DEFAULT_DIALOG_STYLE):
        # Instead of calling wx.Dialog.__init__ we precreate the dialog
        # so we can set an extra style that must be set before
        # creation, and then we create the GUI dialog using the Create
        # method.
        #pre = wx.PreDialog()
        #pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        #pre.Create(parent, ID, title, pos, size, style)

        # This next step is the most important, it turns this Python
        # object into the real wrapper of the dialog (instead of pre)
        # as far as the wxPython extension is concerned.
        #self.PostCreate(pre)
        wx.Dialog.__init__(self, id=ID, name=u'AutoCorrDlg',
              parent=parent, size=size, style=style, title=title)

        # Now continue with the normal construction of the dialog
        # contents
        self.init_ctrls(parent)


    def init_ctrls(self, parent):
        self.ReplaceLabel = wx.StaticTextCtrl(self, 'Replace')
