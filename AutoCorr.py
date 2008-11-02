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
# $Revision: 1.3 $
# $Date: 2008/11/02 22:58:13 $
# $Author: marcin201 $
#-------------------------------------------------------------------------------
import codecs
import XMLDoc

debug_save = False

class AutoCorr:
    def __init__(self):
        self.ReplaceWithList = []
        self.EnableState = True

    def InsertItem(self, replaceStr, withStr):
        i = 0
        for itemFind, itemReplace in self.ReplaceWithList:
            if itemFind > replaceStr:
                break
            i += 1
        self.ReplaceWithList.insert(i, (replaceStr, withStr))

        return i

    def ReplaceItem(self, index, replaceStr, withStr):
        self.ReplaceWithList[index] = (replaceStr, withStr)

    def DeleteItem(self, index):
        self.ReplaceWithList.pop(index)

    def FindReplace(self, str):
        if self.EnableState == False:
            return str

        for replaceStr, withStr in self.ReplaceWithList:
            i = str.find(replaceStr)
            start = 0
            while i >= 0 and start+i+len(replaceStr) < len(str):
                char = str[start+i+len(replaceStr)]
                # with the string only if following and previous character is a a white space
                if char.isspace() and (i == 0 or str[i-1].isspace()):
                    print i
                    print str[i-1]
                    str = str.replace(replaceStr, withStr, 1)
                    start = i+len(withStr)
                else:
                    start = i+len(replaceStr)
                i = str[start:].find(replaceStr)

        return str

    def GetItem(self, index):
        return self.ReplaceWithList[index]

    def GetItems(self):
        return self.ReplaceWithList

    def Enable(self):
        self.EnableState = True

    def Disable(self):
        self.EnableState = False

    def GetSetEnable(self):
        return self.EnableState

    def FindReplaceStr(self, str):
        i = 0
        found = -1
        for replaceStr, withStr in self.ReplaceWithList:
            if str == replaceStr:
                found = i
                break
            i += 1

        return found


    def GenerateTestData(self):
        item = (u"alpha", u"\u03B1")
        self.ReplaceWithList.append(item)
        item = (u"beta", u"\u03B2")
        self.ReplaceWithList.append(item)
        item = (u"delta", u"\u03B4")
        self.ReplaceWithList.append(item)
        item = (u">=", u"\u2265")
        self.ReplaceWithList.append(item)
        item = (u"<=", u"\u2264")
        self.ReplaceWithList.append(item)

        self.ReplaceWithList.sort()

    def Save(self, filename):
        doc = XMLDoc.XMLDocument()

        root = doc.add('data')

        # Add enable
        enableItem = root.add('enable')
        if self.EnableState:
            enableItem.addText('True')
        else:
            enableItem.addText('False')

        # Add item list
        for r,w in self.ReplaceWithList:
            item = root.add('item')
            item.add('replace').addText(r)
            item.add('with').addText(w)

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
            for enableItem in root[0].getAll('enable'):
                str = enableItem.getText()
                if str == 'True':
                    self.EnableState = True
                else:
                    self.EnableState = False

            # Erase all data
            self.ReplaceWithList = []

            # Cards
            for item in root[0].getAll('item'):
                for replaceItem in item.getAll('replace'):
                    replaceStr = replaceItem.getText()
                for withItem in item.getAll('with'):
                    withStr = withItem.getText()

                    self.ReplaceWithList.append((replaceStr, withStr))

        self.ReplaceWithList.sort()


    def PrintList(self):
        for f,r in self.ReplaceWithList:
            print f, r
