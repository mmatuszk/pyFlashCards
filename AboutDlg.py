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

import wx
import wx.html as html
import configparser
import os

ID_ABOUT_DLG = wx.Window.NewControlId()

revcfg_filename = 'rev.cfg'

license_str = """
<html>
<body>
<h3>Credits</h3>
Marcin Matuszkiewicz
<h3>License</h3>
Copyright (C) 2006 Marcin Matuszkiewicz<br>
pyFlashCards comes with ABSOLUTELY NO WARRANTY.  
This is free software, and you are welcome
to redistribute it under certain conditions.
</body>
<html>
"""

class AboutDlg(wx.Dialog):
    def __init__(self, parent, runtimepath):
        wx.Dialog.__init__(self, parent, ID_ABOUT_DLG, 'About pyFlashCards')

        sizer = wx.BoxSizer(wx.VERTICAL)

        # Ensure the image path is correct and file exists
        # Construct the full path to the image
        imagePath = os.path.join(runtimepath, 'icons', 'pyFlashCards2.png')
        imagePath = os.path.normpath(imagePath)

        img = wx.Image(imagePath, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        logo = wx.StaticBitmap(self, -1, img)

        title = wx.StaticText(self, -1, 'pyFlashCards %d.%d.%d' % self.GetVersion())
        f = title.GetFont()
        f.SetPointSize(15)
        title.SetFont(f)

        license = html.HtmlWindow(self, -1, size=(500, 300))
        license.SetPage(license_str)

        button = wx.Button(self, wx.ID_OK, 'OK')

        sizer.Add(logo, 0, wx.CENTER, 10)
        sizer.Add(title, 0, wx.ALL | wx.CENTER, 10)
        sizer.Add(license, 0, wx.ALL | wx.CENTER, 10)
        sizer.Add(button, 0, wx.ALL | wx.CENTER, 10)

        self.SetSizerAndFit(sizer)

    def GetVersion(self):
        config = configparser.ConfigParser()
        config.read(revcfg_filename)

        # Parse configuration file
        try:
            major = int(config.get('rev', 'major'))
            minor = int(config.get('rev', 'minor'))
            build = int(config.get('rev', 'build'))
        except configparser.NoSectionError as sec:
            print('No section:', sec)
            return 0, 0, 0
        except configparser.NoOptionError as opt:
            print('No option', opt)
            return 0, 0, 0

        return (major, minor, build)