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
# $Source: /cvsroot/pyflashcards/pyFlashCards/AutoCorr.py,v $
# $Revision: 1.2 $
# $Date: 2008/11/01 15:53:24 $
# $Author: marcin201 $
#-------------------------------------------------------------------------------
import codecs
import XMLDoc

debug_save = False

class AutoCorr:
    def __init__(self):
        self.FindReplaceList = []

    def FindReplace(self, str):
        for findStr, replaceStr in self.FindReplaceList:
            i = str.find(findStr)
            start = 0
            while i >= 0:
                char = str[start+i+len(findStr)]
                # replace the string only if following character is a a white space
                if char.isspace():
                    str = str.replace(findStr, replaceStr, 1)
                    start = i+len(replaceStr)
                else:
                    start = i+len(findStr)
                i = str[start:].find(findStr)

        return str

    def GenerateTestData(self):
        item = (u"alpha", u"\u03B1")
        self.FindReplaceList.append(item)
        item = (u"beta", u"\u03B2")
        self.FindReplaceList.append(item)
        item = (u"beta-blocker", u"\u03B2-blocker")
        self.FindReplaceList.append(item)
        item = (u"delta", u"\u03B4")
        self.FindReplaceList.append(item)
        item = (u"delta", u"\u03B4")
        self.FindReplaceList.append(item)
        item = (u">=", u"\u2265")
        self.FindReplaceList.append(item)
        item = (u"<=", u"\u2264")
        self.FindReplaceList.append(item)

    def Save(self, filename):
        doc = XMLDoc.XMLDocument()

        root = doc.add('data')

        # Add chapter list
        for f,r in self.FindReplaceList:
            item = root.add('item')
            item.add('find').addText(f)
            item.add('replace').addText(r)
        # Write the document to file
        f = codecs.open(filename, 'w', 'utf_8')
        doc.writexml(f)
        f.close()

        if debug_save:
            f = codecs.open('debug.xml', 'w', 'utf_8')
            doc.writexml(f, newl='\n')
            f.close()

    def Load(self, filename):
        doc = XMLDoc.XMLDocument()
        doc.parse(filename)

        root = doc.getAll('data')

        if root:
            # Erase all data
            self.FindReplaceList = []

            # Cards
            for item in root[0].getAll('item'):
                for find in item.getAll('find'):
                    findStr = find.getText()
                for replace in item.getAll('replace'):
                    replaceStr = replace.getText()

                    self.FindReplaceList.append((findStr, replaceStr))

        self.FindReplaceList.sort()
