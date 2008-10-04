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
# $Source: /cvsroot/pyflashcards/pyFlashCards/FlashCard.py,v $
# $Revision: 1.13 $
# $Date: 2008/10/04 21:38:25 $
# $Author: marcin $
#-------------------------------------------------------------------------------
import fileinput, codecs, os, copy, sys
import XMLDoc
import htmlDoc
import random

if sys.platform == 'win32':
    zipcmd='7z'
elif sys.platform == 'darwin':
    zipcmd = './7za.mac'
else:
    zipcmd='./7z'

debug_save = False

DefaultBoxSize = [10, 20, 50, 100, 250, 500, 1000, 2000, 4000, 10000]
BoxNum = len(DefaultBoxSize)

ImportTypeList  = ['Text file (UTF8) - cards', 'XML file']
ImportWildcard  = ['Text files (*.txt)|*.txt', 'XML files (*.xml)|*.xml']
ExportTypeList  = ['XML file - chapter', 'HTML file - chapter']
ExportWildcard  = ['XML files (*.xml)|*.xml', 'HTML files (*.html)|*.html']
ExportExt       = ['xml', 'html']

# Commands that can be used in front and back text of cards
nab_cmd = '{nab}'
ab_cmd  = '{ab}'

def lindices(list):
    return range(len(list))

def DetectFileEncoding(filename):
    f = open(filename, 'r')
    c0 = f.read(1)
    c1 = f.read(1)
    c2 = f.read(1)

    if c0 == '' or c1 == '' or c2 == '':
        return 'ascii'
    else:
        b0 = ord(c0)
        b1 = ord(c1)
        b2 = ord(c2)

    if b0 == 0xef and b1 == 0xbb or b2 == 0xbf:
        return 'utf_8'
    else:
        # Assume ascii even though other encodings are possible
        return 'ascii'

def GetExportExt(exporttype):
    for i, t in zip(range(len(ExportTypeList)), ExportTypeList):
        if exporttype == t:
            return ExportExt[i]

    return ''

def GetExportWildcard(exporttype):
    for i, t in zip(range(len(ExportTypeList)), ExportTypeList):
        if exporttype == t:
            return ExportWildcard[i]

    return ''

class FlashCardError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

    def getValue(self):
        return self.value

class FlashCard:
    def __init__(self, FrontText, BackText):
        self.Chapter = None
        self.FrontText = FrontText
        self.BackText = BackText
        self.FrontImage = None
        self.BackImage = None
        self.box = -1

#    def __copy__(self):
#        new = FlashCard()
#        new.FrontText = self.FrontText
#        new.BackText = self.BackText
#        new.FrontImage = self.FrontImage
#        new.BackImage = self.FrontImage
#        new.box = self.box

    def SetFrontText(self, text):
        self.FrontText = text

    def SetBackText(self, text):
        self.BackText = text
        
    def SetBothSides(self, FrontText, BackText):
        self.FrontText = FrontText
        self.BackText = BackText

    def SetBox(self,  box):
        self.box = box

    def SetChapter(self, Chapter):
        self.Chapter = Chapter

    def SetFrontImage(self, image):
        self.FrontImage = image

    def SetBackImage(self, image):
        self.BackImage = image

    def GetFrontImage(self):
        return self.FrontImage

    def GetBackImage(self):
        return self.BackImage

    def GetChapter(self):
        return self.Chapter

    def GetBox(self):
        return self.box
        
    def GetBothSides(self):
        return (self.FrontText, self.BackText)

    def GetFrontText(self):
        return self.FrontText

    def GetBackText(self):
        return self.BackText

    def GetFrontHtml(self, face=None, size=5):
        autobreak = True

        str = "<html><body>"
        #str += '<meta content="text/html"; charset="UTF-8">'
        if self.FrontImage:
            str += "<img src='%s'>" % self.FrontImage
        str += '<p><font'
        if face:
            str+=' face="'+face+'"'
        str += ' size=%d>' % size
        for line in self.FrontText.split('\n'):
            cmd = line.lstrip().rstrip()
            if cmd == nab_cmd:
                autobreak = False
                continue
            elif cmd == ab_cmd:
                autobreak = True
                continue

            if autobreak:
                str += line+'<br>'
            else:
                str += line

        str += "</font></p></body></html>"

        return str

    def GetBackHtml(self, face=None, size=5):
        autobreak = True

        str = "<html><body>"
        #str += '<meta content="text/html"; charset="UTF-8">'
        if self.BackImage:
            str += "<img src='%s'>" % self.BackImage
        str += '<p><font'
        if face:
            str+=' face="'+face+'"'
        str += ' size=%d>' % size
        for line in self.BackText.split('\n'):
            cmd = line.lstrip().rstrip()
            if cmd == nab_cmd:
                autobreak = False
                continue
            elif cmd == ab_cmd:
                autobreak = True
                continue

            if autobreak:
                str += line+'<br>'
            else:
                str += line

        str += "</font></p></body></html>"

        return str

    def FrontTextFind(self, str, case=False):
        if case:
            FrontText = self.FrontText
        else:
            str = str.lower()
            FrontText = self.FrontText.lower()

        return FrontText.find(str)

    def BackTextFind(self, str, case=False):
        if case:
            BackText = self.BackText
        else:
            str = str.lower()
            BackText = self.BackText.lower()

        return BackText.find(str)


class FlashCardBox:
    def __init__(self, id, MaxItems=-1):
        self.id = id
        self.MaxItems = MaxItems
        self.list = []

    #--------------------------------------------------------------------------
    # Function adds a card to the end of the list.  If the add was succesfull
    # function returns True and False in case of a failure.
    # Set force to False to ingnore size restriction
    #--------------------------------------------------------------------------
    def AddCard(self, card, force=False):
        if self.IsFull() and force == False:
            return False

        card.SetBox(self.id)
        self.list.append(card)
        return True
    
    #--------------------------------------------------------------------------
    # Function adds cards to the end of the list.  It returns the number of
    # items added.  If more items are attempted to be added than the list can
    # contain, it will add items that can be fit and ignore the rest.
    #--------------------------------------------------------------------------
    def AddCards(self, cards):
        count = 0
        for c in card:
            if self.AddCard():
                count += 1
            else:
                break

        return count

    def GetCards(self):
        return self.list 

    def GetId(self):
        return self.id

    def GetCardCount(self):
        return len(self.list)

    def SetCapacity(self, max):
        self.MaxItems = max

    def GetCapacity(self):
        print 'GetCapacity ', self.MaxItems
        return self.MaxItems

    def RemoveCard(self, index):
        self.list[index].SetBox(-1)
        del self.list[index]

    #--------------------------------------------------------------------------
    # Function returns the first card from the list and removes it.
    #--------------------------------------------------------------------------
    def PopCard(self):
        if len(self.list) == 0:
            return None

        card = self.list[0]
        del self.list[0]
        return card

    def GetAllCards(self):
        return self.list

    def IsFull(self):
        if len(self.list) >= self.MaxItems:
            return True
        else:
            return False


class FlashCardSet:
    def __init__(self):
        self.tmpdir = os.tempnam()
        self.datafile = 'data.xml'
        self.datafile_abs = os.path.join(self.tmpdir, 'data.xml')
        self.picdir = 'Pictures'
        self.picdir_abs = os.path.join(self.tmpdir, 'Pictures')
        self.MakeTmpDir()
        # Create other variables using the ClearAllData function.
        self.ClearAllData()

        # Initialize import map
        self.ImportMap = {}
        self.ImportMap[ImportTypeList[0]] = self.ImportCards
        self.ImportMap[ImportTypeList[1]] = self.ImportXML

        # Initizalize export map
        self.ExportMap = {}
        self.ExportMap[ExportTypeList[0]] = self.ExportXML
        self.ExportMap[ExportTypeList[1]] = self.ExportHTML
        #self.ExportMap[ExportTypeList[1]] = self.ExportHTML2

    def Close(self):
        self.RemoveTmpDir()

    def ClearAllData(self):
        self.ChapterList = []    
        self.ChapterNum = {}
        self.SelectedChapterList = []
        self.AvailableChapterList = []
        self.Cards = {}
        self.TestSet = TestSet()
        self.saved = True
        self.NextImage = 1
        self.FrontFontFace = None
        self.FrontFontSize = 5
        self.BackFontFace = None
        self.BackFontSize = 5
        # Study box determines which box cards are pulled from
        # 0 - use all boxes
        # 1 - only box 1
        # 2 - only box 2
        # ...
        # 10 - only box 10
        self.StudyBox = 0

    def MakeTmpDir(self):
        self.RemoveTmpDir()
        os.mkdir(self.tmpdir)
        os.mkdir(self.picdir_abs)

    def RemoveTmpDir(self):
        print "Removing temporary directory"
        # Check if temp directory exisits
        if os.path.exists(self.tmpdir):
            for root, dirs, files in os.walk(self.tmpdir, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))

            os.rmdir(self.tmpdir)

    def AddChapter(self, chapter, available = True):
        self.saved = False
        if chapter not in self.ChapterList:
            self.ChapterList.append(chapter)
            self.ChapterNum[chapter] = len(self.ChapterList)
            self.Cards[chapter] = []
            if available:
                self.AvailableChapterList.append(chapter)
        else:
            raise FlashCardError("Chapter '%s' already exisits" % chapter)

    def RenameChapter(self, OldChapter, NewChapter):
        self.saved = False
        if OldChapter not in self.ChapterList:
            raise FlashCardError("Chapter '%s' does not exist" % OldChapter)

        # Change the chapter for all the cards
        for card in self.Cards[OldChapter]:
            card.SetChapter(NewChapter)

        # Change the key in cards dictionary
        tmp = self.Cards[OldChapter]
        del self.Cards[OldChapter]
        self.Cards[NewChapter] = tmp

        # Change the key in chapter numbers dictionary
        tmp = self.ChapterNum[OldChapter]
        del self.ChapterNum[OldChapter]
        self.ChapterNum[NewChapter]=tmp

        # Change chapter in chapter list
        for chapter, i in zip(self.ChapterList, range(len(self.ChapterList))):
            if chapter == OldChapter:
                self.ChapterList[i] = NewChapter
                break

        # Change chapter in available chapters list
        for chapter, i in zip(self.AvailableChapterList, range(len(self.AvailableChapterList))):
            if chapter == OldChapter:
                self.AvailableChapterList[i] = NewChapter
                break

        # Change chapter in selected chapters list
        for chapter, i in zip(self.SelectedChapterList, range(len(self.SelectedChapterList))):
            if chapter == OldChapter:
                self.SelectedChapterList[i] = NewChapter
                break

    def RemoveChapter(self, chapter):
        self.saved = False
        if chapter not in self.ChapterList:
            raise FlashCardError("Chapter '%s' does not exist" % chapter)

        if chapter in self.SelectedChapterList:
            # Remove chapter's cards from the TestSet
            self.NotLearnChapter(chapter)
            # Remove chapter from the selected chapter list
            index = self.GetSelectedChapterIndex(chapter)
            del self.SelectedChapterList[index]
        else:
            # Remove the chapter from the available chapter list
            index = self.GetAvailableChapterIndex(chapter)
            del self.AvailableChapterList[index]

        # Remove chapter from chapter list
        index = self.GetChapterIndex(chapter)
        del self.ChapterList[index]
        # Remove chapter's cards
        del self.Cards[chapter]
        # Removed chapter number
        del self.ChapterNum[chapter]
        self.RenumberChapters()

    def RenumberChapters(self):
        self.saved = False
        for chapter, i in zip(self.ChapterList, range(len(self.ChapterList))):
            self.ChapterNum[chapter] = i+1

    def AddCard(self, chapter, card, check_selected = True):
        # Mark data as dirty
        self.saved = False

        # Add the card to the database
        card.SetChapter(chapter)
        self.Cards[chapter].append(card)

        # If chapter is selected the card needs to be added to the test set
        if check_selected and chapter in self.SelectedChapterList:
            self.TestSet.AddCard(card)
        
    def AddCards(self, chapter, cards):
        self.saved = False
        for c in cards:
            self.AddCard(chapter, card)

    def LearnChapter(self, chapter):
        self.saved = False
        self.TestSet.AddChapter(chapter)
        self.TestSet.AddCards(self.Cards[chapter])

    def NotLearnChapter(self, chapter):
        self.saved = False
        self.TestSet.RemoveCards(self.Cards[chapter])
        self.TestSet.RemoveChapterFromPool(chapter)
            
    def DeleteCard(self, chapter, index):
        self.saved = False
        card = self.Cards[chapter][index]
        if card.GetChapter() in self.SelectedChapterList:
            self.TestSet.RemoveCard(card)

        if card.GetFrontImage():
            os.remove(self.GetFrontImage())

        if card.GetBackImage():
            os.remove(self.GetBackImage())

        del self.Cards[chapter][index]
            
    def ModifyCard(self, chapter, index, card):
        self.saved = False
        FrontText, BackText = card.GetBothSides()
        self.Cards[chapter][index].SetBothSides(FrontText, BackText)
        self.Cards[chapter][index].SetFrontImage(card.GetFrontImage())
        self.Cards[chapter][index].SetBackImage(card.GetBackImage())

    def MoveCard(self, chapter, index, NewChapter):
        card = self.Cards[chapter][index]
        if card.GetChapter() in self.SelectedChapterList:
            self.TestSet.RemoveCard(card)
        del self.Cards[chapter][index]

        self.AddCard(NewChapter, card)

    def GetCard(self, chapter, index):
        return self.Cards[chapter][index]

    def GetCardCopy(self, chapter, index):
        return copy.copy(self.Cards[chapter][index])

    def GetChapters(self):
        return self.ChapterList

    def GetChapterIndex(self, chapter):
        for c, i in zip(self.ChapterList, range(len(self.ChapterList))):
            if c == chapter:
                return i

        raise FlashCardError("Chapter '%s' does note exist" % chapter)

    def GetChapterCardCount(self, chapter):
        return len(self.Cards[chapter])

    def GetChapterCount(self):
        return len(self.ChapterList)

    def GetChapterLabel(self, chapter):
        return 'Chapter %d' % self.ChapterNum[chapter]

    def GetSelectedChapters(self):
        return self.SelectedChapterList

    def GetSelectedChapterIndex(self, chapter):
        for c, i in zip(self.SelectedChapterList, range(len(self.SelectedChapterList))):
            if c == chapter:
                return i

        raise FlashCardError("Chapter '%s' does note exist" % chapter)

    def GetAvailableChapters(self):
        return self.AvailableChapterList

    def GetAvailableChapterIndex(self, chapter):
        for c, i in zip(self.AvailableChapterList, range(len(self.AvailableChapterList))):
            if c == chapter:
                return i

        raise FlashCardError("Chapter '%s' does note exist" % chapter)
    
    def GetChapterCards(self, chapter):
        return self.Cards[chapter]

    def GetChapterCardCount(self, chapter):
        return len(self.Cards[chapter])

    def GetCard(self, chapter, index):
        return self.Cards[chapter][index]

    def GetCardIndex(self, card):
        chapter = card.GetChapter()
        for c, i in zip(self.Cards[chapter], lindices(self.Cards[chapter])):
            if c == card:
                return i

        raise FlashCardError("Card not found")
    
    def GetBoxes(self):
        return self.TestSet.GetBoxes()

    def GetBoxCardCount(self, index):
        return self.TestSet.GetBoxCardCount(index)

    def SetBoxCapacity(self, index, max):
        self.TestSet.SetBoxCapacity(index, max)

    def GetBoxCapacity(self, index):
        return self.TestSet.GetBoxCapacity(index)

    def GetTestCardsCount(self):
        return self.TestSet.GetCardCount()

    def GetTestCard(self):
        return self.TestSet.GetTestCard()

    #---------------------------------------------------------------------------
    # Function will remove the chapter refered to by ChapterIndex from
    # AvailalbeChaptersList and move it to SelectedChaptersList.  It will also
    # add cards from that chapter to TestSet.
    #---------------------------------------------------------------------------
    def SelectChapter(self, ChapterIndex):
        self.saved = False
        chapter = self.AvailableChapterList[ChapterIndex]
        del self.AvailableChapterList[ChapterIndex]
        self.SelectedChapterList.append(chapter)
        self.LearnChapter(chapter)

    def DeselectChapter(self, ChapterIndex):
        self.saved = False
        chapter = self.SelectedChapterList[ChapterIndex]

        self.NotLearnChapter(chapter)

        del self.SelectedChapterList[ChapterIndex]
        num = self.ChapterNum[chapter]
        if num == 1:
            # If it is the first chapter we need special treatment
            self.AvailableChapterList[:0] = [chapter]
            i = 0
        else:
            i = 0
            c = None
            for c in self.AvailableChapterList:
                if self.ChapterNum[c] > num:
                    break
                i += 1

            if not c:
                # There is not chapters in available chapters list
                self.AvailableChapterList.append(chapter)
            elif self.ChapterNum[c] > num:
                self.AvailableChapterList[i:i] = [chapter]
            else:
                self.AvailableChapterList[i+1:i+1] = [chapter]

        return i

    def NextTestCard(self):
        self.saved = False
        return self.TestSet.NextTestCard()

    def PromoteTestCard(self):
        self.saved = False
        self.TestSet.PromoteTestCard()

    def PromoteTestCardToLastBox(self):
        self.saved = False
        self.TestSet.PromoteTestCardToLastBox()

    def DemoteTestCard(self):
        self.saved = False
        self.TestSet.DemoteTestCard()

    def GetTestCard(self):
        self.saved = False
        return self.TestSet.GetTestCard()

    def GetNextImageName(self):
        image = os.path.join(self.picdir, '%07d.jpg' % self.NextImage)
        self.NextImage += 1
        return image

    def SetFrontFontFace(self, face):
        self.FrontFontFace = face

    def GetFrontFontFace(self):
        return self.FrontFontFace

    def SetFrontFontSize(self, size):
        self.FrontFontSize = size

    def GetFrontFontSize(self):
        return self.FrontFontSize

    def SetBackFontFace(self, face):
        self.BackFontFace = face

    def GetBackFontFace(self):
        return self.BackFontFace

    def SetBackFontSize(self, size):
        self.BackFontSize = size

    def GetBackFontSize(self):
        return self.BackFontSize

    def SetStudyBox(self, box):
        self.StudyBox = box

    def GetStudyBox(self):
        return self.StudyBox

    def RandomizePool(self):
        self.TestSet.RandomizePool()

    def IsSaved(self):
        return self.saved

    def Save(self, filename):
        self.SaveData(self.datafile)

        if os.path.exists(filename):
            os.remove(filename)

        # Make the zip command
        cmd = 'tar -cjf %s -C % % %' % (filename, self.tmpdir, self.picdir, self.datafile)
        print cmd

        self.saved = True

    def Load(self, filename):    
        print "Load: ", filename
        self.RemoveTmpDir()
        #cmd = zipcmd+' x '
        cmd = zipcmd+' -xjf'
        cmd += '"'+filename+'"'
        #cmd += ' -o'+self.tmpdir
        print cmd
        stdin, stdout, stderr = os.popen3(cmd)
        # read stdout to make sure that the command finishes before we continue
        # It worked without reading on windows, but on Linux it we tried to read
        # tmp1/data.xml before the extract command completed
        out = stdout.read()
        err = stderr.read()
        print out
        print err
        #self.LoadData(self.datafile)
        self.LoadData('tmp1/data.xml')

        self.saved = True

    def SaveData(self, filename):
        doc = XMLDoc.XMLDocument()

        root = doc.add('data')

        # Add chapter list
        child = root.add('chapter_list')
        for chapter in self.ChapterList:
            child.add('chapter').addText(chapter)

        # Add available chapter list
        child = root.add('available_chapter_list')
        for chapter in self.AvailableChapterList:
            child.add('chapter').addText(chapter)

        # Add selected chapter list
        child = root.add('selected_chapter_list')
        for chapter in self.SelectedChapterList:
            child.add('chapter').addText(chapter)

        # Add cards
        cardsNode = root.add('card_list')
        for chapter in self.ChapterList:
            for card in self.Cards[chapter]:
                node = cardsNode.add('card')
                node.add('front_text').addText(card.GetFrontText())
                node.add('back_text').addText(card.GetBackText())
                if card.FrontImage:
                    node.add('front_image').addText(card.GetFrontImage())
                if card.BackImage:
                    node.add('back_image').addText(card.GetBackImage())
                node.add('chapter').addText(chapter)

        # Add boxes
        boxesNode = root.add('box_list')
        for box in self.TestSet.GetBoxes():
            node = boxesNode.add('box')
            node.add('max_items').addText(`box.GetCapacity()`)
            for card in box.GetCards():
                node1 = node.add('card')
                node1.add('chapter').addText(card.GetChapter())
                # Find the index of the card in the card list
                chapter = card.GetChapter()
                for i in range(self.GetChapterCardCount(chapter)):
                    if card == self.GetCard(chapter, i):
                        break

                if card == self.GetCard(chapter, i):
                    node1.add('index').addText(`i`)
                else:
                    node1.add('index').addText(`-1`)

        # The test card
        learningCardNode = root.add('test_card')
        card = self.TestSet.GetTestCard()
        boxIndex = self.TestSet.GetTestCardBox()
        if card == None:
            learningCardNode.add('chapter').addText('None')
            learningCardNode.add('card_index').addText('-1')
            learningCardNode.add('box_index').addText('-1')
        else:
            chapter = card.GetChapter()
            learningCardNode.add('chapter').addText(chapter)

            for i in range(self.GetChapterCardCount(chapter)):
                if card == self.GetCard(chapter, i):
                    break

            if card == self.GetCard(chapter, i):
                learningCardNode.add('card_index').addText(`i`)
                learningCardNode.add('box_index').addText(`boxIndex`)
            else:
                learningCardNode.add('card_index').addText(`-1`)
                learningCardNode.add('box_index').addText(`boxIndex`)

        # Add next image index
        next_image = root.add('next_image')
        next_image.addText(`self.NextImage`)

        # Front front information
        FontNode = root.add('front_font')
        if self.FrontFontFace:
            FontNode.add('face').addText(self.FrontFontFace)
        FontNode.add('size').addText(`self.FrontFontSize`)

        # Back front information
        FontNode = root.add('back_font')
        if self.BackFontFace:
            FontNode.add('face').addText(self.BackFontFace)
        FontNode.add('size').addText(`self.BackFontSize`)

        # Write the document to file
        f = codecs.open(filename, 'w', 'utf_8')
        doc.writexml(f)
        f.close()

        if debug_save:
            f = codecs.open('debug.xml', 'w', 'utf_8')
            doc.writexml(f, newl='\n')
            f.close()


    def LoadData(self, filename):
        doc = XMLDoc.XMLDocument()
        doc.parse(filename)

        root = doc.getAll('data')

        if root:
            # Erase all data
            self.ClearAllData()
            # Chapters
            for chapter_list in root[0].getAll('chapter_list'):
                for chapter in chapter_list.getAll('chapter'):
                    self.AddChapter(chapter.getText(), False)

            # Available chapters
            for available_chapter_list in root[0].getAll('available_chapter_list'):
                for chapter in available_chapter_list.getAll('chapter'):
                    self.AvailableChapterList.append(chapter.getText())

            # Selected chapters
            for selected_chapter_list in root[0].getAll('selected_chapter_list'):
                for chapter in selected_chapter_list.getAll('chapter'):
                    self.SelectedChapterList.append(chapter.getText())

            # Cards
            for card_list in root[0].getAll('card_list'):
                for cardNode in card_list.getAll('card'):
                    for front in cardNode.getAll('front_text'):
                        frontText = front.getText()
                    for back in cardNode.getAll('back_text'):
                        backText = back.getText()

                    card = FlashCard(frontText, backText)        

                    for front in cardNode.getAll('front_image'):
                        frontImage = front.getText()
                        card.SetFrontImage(frontImage)
                    for back in cardNode.getAll('back_image'):
                        backImage = back.getText()
                        card.SetBackImage(backImage)

                    for chapter in cardNode.getAll('chapter'):
                        chapterText = chapter.getText()
                    # When adding the card, do not add it to the pool even if the chapter is selected
                    # Cards will be loaded into learning boxes later
                    self.AddCard(chapterText, card, False)
                    
            # Boxes
            for box_list in root[0].getAll('box_list'):
                # Create a new test set
                self.TestSet = TestSet([])
                # Add selected chapters to the pool
                for chapter in self.SelectedChapterList:
                    self.TestSet.AddChapter(chapter)
                for box in box_list.getAll('box'):
                    for max_items in box.getAll('max_items'):
                        MaxItems = int(max_items.getText())
                        if MaxItems < 0:
                            # We are reading the pool.  The pool is created when the 
                            # TestSet is created therefore it is not necessary to 
                            # add a new box
                            BoxIndex = 0
                        else:
                            BoxIndex = self.TestSet.AddBox(MaxItems)
                    for card in box.getAll('card'):
                        for chapter in card.getAll('chapter'):
                            chapterText = chapter.getText()
                        for index in card.getAll('index'):
                            IndexInt = int(index.getText())

                        card = self.GetCard(chapterText, IndexInt)
                        self.TestSet.PlaceCard(BoxIndex, card)

            # Test card
            for test_card in root[0].getAll('test_card'):
                for box_index in test_card.getAll('box_index'):
                    BoxIndexInt = int(box_index.getText())

                if BoxIndexInt < 0:
                    self.TestSet.SetTestCard(None)
                    self.TestSet.SetTestCardBox(-1)
                else:
                    for chapterNode in test_card.getAll('chapter'):
                        chapter = chapterNode.getText()

                    for card_index in test_card.getAll('card_index'):
                        CardIndexInt = int(card_index.getText())

                    if CardIndexInt < 0:
                        self.TestSet.SetTestCard(None)
                        self.TestSet.SetTestCardBox(-1)
                    else:
                        self.TestSet.SetTestCard(self.GetCard(chapter, CardIndexInt))
                        self.TestSet.SetTestCardBox(BoxIndexInt)
                        self.GetCard(chapter, CardIndexInt).SetBox(BoxIndexInt)

            # Next image
            for next_image in root[0].getAll('next_image'):
                self.NextImage = int(next_image.getText())

            # Load front font information
            for FontNode in root[0].getAll('front_font'):
                for FaceNode in FontNode.getAll('face'):
                    self.FrontFontFace = FaceNode.getText()
                    print self.FrontFontFace
                for SizeNode in FontNode.getAll('size'):
                    self.FrontFontSize = int(SizeNode.getText())

            for FontNode in root[0].getAll('back_font'):
                for FaceNode in FontNode.getAll('face'):
                    self.BackFontFace = FaceNode.getText()
                for SizeNode in FontNode.getAll('size'):
                    self.BackFontSize = int(SizeNode.getText())

    def Import(self, type, filename, chapter):
        if type not in self.ImportMap.keys():
            return 0

        return self.ImportMap[type](filename, chapter)

    def Export(self, type, filename, chapter):
        if type not in self.ExportMap.keys():
            return 0

        return self.ExportMap[type](filename, chapter)
                        
    def ImportCards(self, filename, chapter):
        print filename
        question = True
        FrontText = ''
        BackText = ''
        lnsep = '\n'
    
        count = 0

        enc = DetectFileEncoding(filename)

        f = codecs.open(filename, 'r', enc)
        if enc == 'utf_8':
            # Skip the first three bytes which  define encoding
            f.read(3)

        line = f.readline()
        while line != '':
            line = line.rstrip()
            line = line.lstrip()
            
            if len(line) > 0:
                if question:
                    FrontText = line
                    question = False
        
                else:
                    if len(BackText) == 0:
                        BackText = line
                    else:
                        BackText = BackText + lnsep + line
            else:
                question = True
                if len(FrontText) != 0 and len(BackText) != 0:
                    self.AddCard(chapter, FlashCard(FrontText, BackText))
                    count += 1
                    FrontText = ''
                    BackText = ''

            line = f.readline()
        print len(FrontText)
        print len(BackText)
        if len(FrontText) != 0 and len(BackText) != 0:
            print len(FrontText)
            print len(BackText)
            question = True
            self.AddCard(chapter, FlashCard(FrontText, BackText))
            count += 1
            FrontText = ''
            BackText = ''
            
        f.close()

        return count

    def ImportXML(self, filename, chapter):
        count = 0

        if chapter not in self.GetChapters():
            return count

        doc = XMLDoc.XMLDocument()
        doc.parse(filename)

        root = doc.getAll('data')

        if root:
            # Cards
            for card_list in root[0].getAll('card_list'):
                for cardNode in card_list.getAll('card'):
                    for front in cardNode.getAll('front_text'):
                        frontText = front.getText()
                    for back in cardNode.getAll('back_text'):
                        backText = back.getText()

                    card = FlashCard(frontText, backText)        
                    self.AddCard(chapter, FlashCard(frontText, backText))
                    
                    count += 1

        return count

    def ExportXML(self, filename, chapter):
        ct = 0
        doc = XMLDoc.XMLDocument()

        root = doc.add('data')

        cardsNode = root.add('card_list')
        for card in self.Cards[chapter]:
            node = cardsNode.add('card')
            node.add('front_text').addText(card.GetFrontText())
            node.add('back_text').addText(card.GetBackText())
            node.add('chapter').addText(chapter)
            ct += 1

        # Write the document to file
        f = codecs.open(filename, 'w', 'utf_8')
        doc.writexml(f)
        f.close()

        return ct

    def ExportHTML(self, filename, chapter):
        ct = 0
        Tag = htmlDoc.Tag

        doc = htmlDoc.HtmlDocument()
        doc.setHtmlTitle(chapter)

        table=Tag.TABLE(None, '100%', 1, "#000000", 4, 0)
        for card in self.Cards[chapter]:
            tr = Tag.TR(None, "TOP")
            td = Tag.TD(contents=None, width="50%")
            for line in card.GetFrontText().split('\n'):
                td.append(line)
                td.append(Tag.BR())
            tr.append(td)

            td = Tag.TD(contents=None, width="50%")
            for line in card.GetBackText().split('\n'):
                td.append(line)
                td.append(Tag.BR())
            tr.append(td)
                
            table.append(tr)
            ct += 1

        doc.append(table)

        # Write the document to file
        f = codecs.open(filename, 'w', 'utf_8')
        #f = open(filename, 'w')
        f.write(codecs.BOM_UTF8.decode('utf_8'))
        doc.writeHtml(f)
        f.close()
            
        return ct

    # single column, w/ answer below the quesion
    def ExportHTML2(self, filename, chapter):
        ct = 0
        Tag = htmlDoc.Tag

        doc = htmlDoc.HtmlDocument()
        doc.setHtmlTitle(chapter)

        table=Tag.TABLE(None, '100%', 1, "#000000", 4, 0)
        for card in self.Cards[chapter]:
            tr = Tag.TR(None, "TOP")
            td = Tag.TD(contents=None, width="50%")
            for line in card.GetFrontText().split('\n'):
                td.append(line)
                td.append(Tag.BR())
            tr.append(td)
            table.append(tr)

            tr = Tag.TR(None, "TOP")
            td = Tag.TD(contents=None, width="50%")
            for line in card.GetBackText().split('\n'):
                td.append(line)
                td.append(Tag.BR())
            tr.append(td)
            table.append(tr)

            ct += 1

        doc.append(table)

        # Write the document to file
        f = codecs.open(filename, 'w', 'utf_8')
        #f = open(filename, 'w')
        f.write(codecs.BOM_UTF8.decode('utf_8'))
        doc.writeHtml(f)
        f.close()
            
        return ct
    
    #-------------------------------------------------------------------------
    # Export specified chapter to the XML format supported by the
    # FlashCard101 version 3.
    #-------------------------------------------------------------------------
    def ExportFlashCard101(self, filename, chapter):
        f = open(filename, 'w')

#    	if b0 == 0xef and b1 == 0xbb or b2 == 0xbf:
        f.write(codecs.BOM_UTF8)
        f.write('<?xml version="1.0" encoding="utf-8"?>\n')
        f.write('<FlashCards>\n')

        index = 1
        for card in self.Cards[chapter]:
            f.write('<Card number="%d" AimagePath="" QimagePath="">\n' % index)
            f.write('<Question>')
            f.write(card.GetFrontText().encode('utf_8'))
            f.write('</Question>\n')
            f.write('<Answer>')
            f.write(card.GetBackText().encode('utf_8'))
            f.write('</Answer>\n')
            f.write('</Card>\n')

            index += 1

	f.write('</FlashCards>')
	f.close()

	return index


#        doc = XMLDoc.XMLDocument()
#
#        root = doc.add('FlashCards')
#        # Add cards
#        index = 1
#        for card in self.Cards[chapter]:
#            #str = 'number="%d" AimagePath="" QimagePath=""' % index
#            node = root.add2('Card', ['number', 'AimagePath', 'QimagePath'], number="%d" % index, AimagePath="", QimagePath="")
#            #node = root.add('Card', str)
#            node.add('Question').addText(card.GetFrontText())
#            node.add('Answer').addText(card.GetBackText())
#            index += 1
#            
#        # Write the document to file
#        f = codecs.open(filename, 'w', 'utf_8')
#        doc.writexml(f)
#        f.close()
#
#        if debug_save:
#            f = codecs.open('debug.xml', 'w', 'utf_8')
#            doc.writexml(f, newl='\n')
#            f.close()
    
    def GenerateTestData(self):    
        self.ClearAllData()

        for n in range(1,16):
            chapter = 'Chapter %d' % n
            self.AddChapter(chapter)
            front = 'Chapter %d: front' % n
            back = 'Chapter %d: back' % n
            cards = [FlashCard(front + `d`, back + `d`) for d in range(10+n)]
            self.AddCards(chapter, cards)

        self.Cards['Chapter 1'][0].SetFrontText(u'\u6211')


if __name__ == '__main__':
    set = FlashCardSet()

    set.GenerateTestData()
    set.SelectChapter(0)
    set.SelectChapter(0)
    set.Save('test.xml')
    set.Load('test.xml')
