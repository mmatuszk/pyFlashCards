#!/usr/bin/env python
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
# $Source: /cvsroot/pyflashcards/pyFlashCards/pyFlashCards.py,v $
# $Revision: 1.26 $
# $Date: 2009/02/25 03:03:05 $
# $Author: marcin201 $
#-------------------------------------------------------------------------------

import wx
import os, os.path
import types
import configparser
import sys
import webbrowser

import wx.html as html
import wx.adv # wx.adv module contains the Wizard class
import MyArtProvider


from CardManagerDlg import *
from CardBrowserDlg import *
from ChapterManagerDlg import *
from LearningManagerDlg import *
from BoxManagerDlg import *
import AutoCorr
import ViewDlg
import AboutDlg
import FlashCard
import FlashCardDataDisp
import events
import ImportWizard as iw
import ExportWizard as ew

ID_FLASH_CARD_FRAME             = wx.Window.NewControlId()

ID_FILE_NEW                     = wx.Window.NewControlId()
ID_FILE_OPEN                    = wx.Window.NewControlId()
ID_FILE_RECENT_DOCS             = wx.Window.NewControlId()
ID_FILE_CLOSE                   = wx.Window.NewControlId()
ID_FILE_IMPORT                  = wx.Window.NewControlId()
ID_FILE_EXPORT                  = wx.Window.NewControlId()
ID_FILE_SAVE                    = wx.Window.NewControlId()
ID_FILE_SAVE_AS                 = wx.Window.NewControlId()
ID_FILE_EXIT                    = wx.Window.NewControlId()

ID_CARDS_CARD_MANAGER           = wx.Window.NewControlId()
ID_CARDS_CARD_BROWSER           = wx.Window.NewControlId()
ID_CARDS_EDIT_TEST_CARD         = wx.Window.NewControlId()
ID_CARDS_CHAPTER_MANAGER        = wx.Window.NewControlId()

ID_LEARNING_LEARNING_MANAGER    = wx.Window.NewControlId()
ID_LEARNING_BOX_MANAGER         = wx.Window.NewControlId()
ID_LEARNING_RANDOMIZE           = wx.Window.NewControlId()

ID_TOOLS_VIEW_CH_HTML           = wx.Window.NewControlId()
ID_TOOLS_VIEW_ANS               = wx.Window.NewControlId()
ID_TOOLS_DISP_DATA              = wx.Window.NewControlId()

ID_HELP_CONTENTS                = wx.Window.NewControlId()
ID_HELP_ABOUT                   = wx.Window.NewControlId()

ID_LEARN_SHOW_ANSWER            = wx.Window.NewControlId()
ID_LEARN_KNOW                   = wx.Window.NewControlId()
ID_LEARN_NOT_KNOW               = wx.Window.NewControlId()
ID_LEARN_NOT_AGAIN	            = wx.Window.NewControlId()
ID_LEARN_HIDE_ANSWER            = wx.Window.NewControlId()

ID_TEST_PANEL                   = wx.Window.NewControlId()

ID_TEST_PANEL_STATE_SHOW_NONE       = 0
ID_TEST_PANEL_STATE_SHOW_QUESTION   = 1
ID_TEST_PANEL_STATE_SHOW_ANSWER     = 2

ID_TP_FRONT_FONT_FACE   = wx.Window.NewControlId()
ID_TP_FRONT_FONT_SIZE   = wx.Window.NewControlId()
ID_TP_BACK_FONT_FACE    = wx.Window.NewControlId()
ID_TP_BACK_FONT_SIZE    = wx.Window.NewControlId()

defext = 'ofc'
wildcard = 'Flash Card files (*.%s)|*.%s' % (defext, defext)
ConfigFileName      = 'flashcard.cfg'
AutoCorrFileName    = 'autocorr.xml'

ApplicationName = 'pyFlashCards'

DefaultWinWidth     = 1024
DefaultWinHeight    = 700

# Display modes
mode_default = 1
mode_mini = 2

display_mode = mode_default

TestHtml=\
"""
<html>
<body>
	<img src='Netter_001-a.jpg' height=896 width=600>
</body>
</html>
"""

EmptyHtml="<html></html>"

def AddMenuItemWithImage(menu, id, item, helpString, image):
    if isinstance(image, str):
        img = wx.Image(image, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    else:
        img = image
    item = wx.MenuItem(menu, id, item, helpString)
    item.SetBitmap(img)
    menu.Append(item)  # Updated to use Append instead of AppendItem


myEVT_LP_DATA_CHANGED = wx.NewEventType()
EVT_LP_DATA_CHANGED   = wx.PyEventBinder(myEVT_LP_DATA_CHANGED, 1)

class TestPanelEvent(wx.PyCommandEvent):
    def __init__(self, evtType, id):
        wx.PyCommandEvent.__init__(self, evtType, id)


class FlashCardFrame(wx.Frame):
    def __init__(self, parent, id, help):
        wx.Frame.__init__(self, parent, id, "Flash Cards", size=(800,600))

        self.runtimepath = os.getcwd()

        self.help = help

        self.LoadConfig()
        self.LoadAutoCorr()


        wx.ArtProvider.Push( MyArtProvider.TangoArtProvider(self.runtimepath) )

        iconfile = os.path.join(self.runtimepath, 'icons/pyFlashCards2-32x32.ico')
        icon = wx.Icon(iconfile, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        # Initialize data
        self.DispData = False
        self.CardSet = None
        self.filename = None

        self.CreateStatusBar()
        self.AddMenu()
        self.LoadFileHistory()

        sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.TestPanel = TestPanel(self, ID_TEST_PANEL, self.CardSet)
        self.TestPanel.Show(False)
        #self.TestPanel.StartTest()
        sizer.Add(self.TestPanel, 1, wx.EXPAND)

        self.Bind(EVT_LP_DATA_CHANGED, self.OnTestPanelDataChanged, self.TestPanel)

        self.SetAutoLayout(True)
        self.SetSizerAndFit(sizer)

        self.GenerateTitle()

        w = self.Config.getint('window_size', 'width')
        h = self.Config.getint('window_size', 'height')
        if self.Config.getboolean('window_size', 'max'):
            self.SetSize((w, h))
            self.Maximize()
        else:
            self.SetSize((w, h))

        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.Bind(wx.EVT_SIZE, self.OnSize)

        # Open a test files
        #self.UtilOpenTestFile()

    def LoadCardSet(self, filename):
        self.filename = filename
        self.CardSet.Load(self.filename)
        self.TestPanel.StartTest()

        # Update configuration
        self.Config.set('directories', 'card_dir', os.path.dirname(filename))

        self.EnableDataMenu()

    def LoadConfig(self):
        self.Config = configparser.ConfigParser()

        self.Config.read(GetConfigFileName())

        # Window size
        if not self.Config.has_section('window_size'):
            self.Config.add_section('window_size')
        self.Config.set('window_size', 'max', self.Config.get('window_size', 'max', fallback='false'))
        self.Config.set('window_size', 'width', str(self.Config.getint('window_size', 'width', fallback=DefaultWinWidth)))
        self.Config.set('window_size', 'height', str(self.Config.getint('window_size', 'height', fallback=DefaultWinHeight)))

        # Directories
        home_directory = os.path.expanduser('~')
        if not self.Config.has_section('directories'):
            self.Config.add_section('directories')
        self.Config.set('directories', 'card_dir', self.Config.get('directories', 'card_dir', fallback=home_directory))
        self.Config.set('directories', 'image_dir', self.Config.get('directories', 'image_dir', fallback=home_directory))
        self.Config.set('directories', 'import_dir', self.Config.get('directories', 'import_dir', fallback=home_directory))
        self.Config.set('directories', 'export_dir', self.Config.get('directories', 'export_dir', fallback=home_directory))

        # File History
        if not self.Config.has_section('file_history'):
            self.Config.add_section('file_history')
        self.Config.set('file_history', 'files', self.Config.get('file_history', 'files', fallback=''))

        # Card browser
        if not self.Config.has_section('card_browser'):
            self.Config.add_section('card_browser')
        self.Config.set('card_browser', 'width', str(self.Config.getint('card_browser', 'width', fallback=DefaultWinWidth)))
        self.Config.set('card_browser', 'height', str(self.Config.getint('card_browser', 'height', fallback=DefaultWinHeight)))

        # Card manager
        if not self.Config.has_section('card_manager'):
            self.Config.add_section('card_manager')
        self.Config.set('card_manager', 'width', str(self.Config.getint('card_manager', 'width', fallback=DefaultWinWidth)))
        self.Config.set('card_manager', 'height', str(self.Config.getint('card_manager', 'height', fallback=DefaultWinHeight)))

    def WriteConfig(self):
        with open(GetConfigFileName(), 'w') as configfile:
            self.Config.write(configfile)

    def LoadAutoCorr(self):
        # create an empty AutoCorr object
        self.autocorr = AutoCorr.AutoCorr()

        # Start with user autocorr file
        filename = GetAutoCorrFileName()

        if os.path.exists(filename):
            self.autocorr.Load(filename)
            return
        else:
            print("Warning: user autocorrect file does not exist")


        # If the user file does not exist, try the application file
        filename = os.path.join(self.runtimepath, 'autocorr', AutoCorrFileName)
        if os.path.exists(filename):
            self.autocorr.Load(filename)
            return
        else:
            print("Warning: application autocorrect file does not exist")


    def WriteAutoCorr(self):
        filename = GetAutoCorrFileName()
        self.autocorr.Save(filename)

    def GenerateTitle(self):
        if not self.CardSet:
            title = ApplicationName
            self.SetTitle(title)
        else:
            if self.filename:
                dir, filename = os.path.split(self.filename)
                title = filename + ' - ' + ApplicationName
                self.SetTitle(title)
            else:
                title = 'Untitled' + ' - ' + ApplicationName
                self.SetTitle(title)

    def AddMenu(self):
        MenuBar = wx.MenuBar()
        #-----------------------------------------------------------------------
        # File menu
        #-----------------------------------------------------------------------
        FileMenu = wx.Menu()
        new_bmp =  wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_MENU)
        AddMenuItemWithImage(FileMenu, ID_FILE_NEW, '&New\tCtrl+N',
                             'Create a new card file',
                             new_bmp)
        open_bmp =  wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_MENU)
        AddMenuItemWithImage(FileMenu, ID_FILE_OPEN, '&Open\tCtrl+O',
                             'Open an existing card file',
                              open_bmp)
        RecentDocsMenu = wx.Menu()
        FileMenu.AppendMenu(ID_FILE_RECENT_DOCS, "Recent Documents", RecentDocsMenu)
        FileMenu.Append(ID_FILE_CLOSE, 'Close', 'Close the card file\tCtrl+W')
        FileMenu.Enable(ID_FILE_CLOSE, False)
        FileMenu.AppendSeparator()
        FileMenu.Append(ID_FILE_IMPORT, 'Import\tCtrl+I', 'Import a card file')
        FileMenu.Enable(ID_FILE_IMPORT, False)
        FileMenu.Append(ID_FILE_EXPORT, 'Export\tCtrl+X', 'Export a card file')
        FileMenu.Enable(ID_FILE_EXPORT, False)
        FileMenu.AppendSeparator()
        save_bmp =  wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_MENU)
        AddMenuItemWithImage(FileMenu, ID_FILE_SAVE, '&Save\tCtrl+S',
                             'Save the card file',
                              save_bmp)
        FileMenu.Enable(ID_FILE_SAVE, False)
        save_as_bmp =  wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE_AS, wx.ART_MENU)
        AddMenuItemWithImage(FileMenu, ID_FILE_SAVE_AS, 'S&ave as',
                             'Save file unde a new name',
                              save_as_bmp)
        FileMenu.AppendSeparator()
        FileMenu.Append(ID_FILE_EXIT, 'E&xit', 'Exit program')
        FileMenu.Enable(ID_FILE_SAVE_AS, False)


        # Add File History
        self.FileHistory = wx.FileHistory()
        self.FileHistory.UseMenu(RecentDocsMenu)

        self.Bind(wx.EVT_MENU, self.OnNew, id=ID_FILE_NEW)
        self.Bind(wx.EVT_MENU, self.OnSave, id=ID_FILE_SAVE)
        self.Bind(wx.EVT_MENU, self.OnSaveAs, id=ID_FILE_SAVE_AS)
        self.Bind(wx.EVT_MENU, self.OnOpen, id=ID_FILE_OPEN)
        self.Bind(wx.EVT_MENU_RANGE, self.OnFileHistory, id=wx.ID_FILE1, id2=wx.ID_FILE9)
        self.Bind(wx.EVT_MENU, self.OnClose, id=ID_FILE_CLOSE)
        self.Bind(wx.EVT_MENU, self.OnImportWizard, id=ID_FILE_IMPORT)
        self.Bind(wx.EVT_MENU, self.OnExportWizard, id=ID_FILE_EXPORT)
        self.Bind(wx.EVT_MENU, self.OnExit, id=ID_FILE_EXIT)

        
        MenuBar.Append(FileMenu, '&File')
        self.FileMenu = FileMenu

        #-----------------------------------------------------------------------
        # Cards menu
        #-----------------------------------------------------------------------
        CardsMenu = wx.Menu()
        CardsMenu.Append(ID_CARDS_CARD_MANAGER, 'Card manager\tCtrl+K',
                                                'Open the card manager')
        CardsMenu.Enable(ID_CARDS_CARD_MANAGER, False)
        CardsMenu.Append(ID_CARDS_CARD_BROWSER, 'Card browser\tCtrl+W',
                                                'Open the card browser')
        CardsMenu.Enable(ID_CARDS_CARD_BROWSER, False)
        CardsMenu.Append(ID_CARDS_EDIT_TEST_CARD, 'Edit test card\tCtrl+E',
                                                'Open card manager and edit test card')
        CardsMenu.Enable(ID_CARDS_EDIT_TEST_CARD, False)
        CardsMenu.Append(ID_CARDS_CHAPTER_MANAGER, 'Chapter manager\tCtrl+P',
                                                'Open the chapter manager')
        CardsMenu.Enable(ID_CARDS_CHAPTER_MANAGER, False)

        MenuBar.Append(CardsMenu, '&Cards')
        self.CardsMenu = CardsMenu

        #-----------------------------------------------------------------------
        # Learning menu
        #-----------------------------------------------------------------------
        LearningMenu = wx.Menu()

        ###
        LearningMenu.Append(ID_LEARNING_LEARNING_MANAGER, 'Learning manager\tCtrl+L',
                                                'Open the learning manager')
        LearningMenu.Enable(ID_LEARNING_LEARNING_MANAGER, False)
        ###
        LearningMenu.Append(ID_LEARNING_BOX_MANAGER, 'Box manager\tCtrl+B',
                                                'Open the box manager')
        LearningMenu.Enable(ID_LEARNING_BOX_MANAGER, False)
        ###
        LearningMenu.Append(ID_LEARNING_RANDOMIZE, 'Randomize pool\tCtrl+R',
                                                'Randomize cards in the pool')
        LearningMenu.Enable(ID_LEARNING_RANDOMIZE, False)

        MenuBar.Append(LearningMenu, '&Learning')
        self.LearningMenu = LearningMenu

        #-----------------------------------------------------------------------
        # Tools menu
        #-----------------------------------------------------------------------
        ToolsMenu = wx.Menu()

        ToolsMenu.Append(ID_TOOLS_VIEW_CH_HTML, "View chapter as html", 
                         'View the chapter as html file in the default browsser')
        ToolsMenu.Enable(ID_TOOLS_VIEW_CH_HTML, False)
        ToolsMenu.Append(ID_TOOLS_VIEW_ANS, "View the answer\tCtrl+V",
                         'View the answer full screen')
        ToolsMenu.Enable(ID_TOOLS_VIEW_ANS, False)
        ToolsMenu.Append(ID_TOOLS_DISP_DATA, 'Display data\tCtrl+D',
                         'Display flash card data')
        ToolsMenu.Enable(ID_TOOLS_DISP_DATA, False)

        MenuBar.Append(ToolsMenu, '&Tools')
        self.ToolsMenu = ToolsMenu

        #-----------------------------------------------------------------------
        # Help menu
        #-----------------------------------------------------------------------
        HelpMenu = wx.Menu()
        HelpMenu.Append(ID_HELP_CONTENTS, 'Contents\tF1')
        HelpMenu.Append(ID_HELP_ABOUT, 'About')
        MenuBar.Append(HelpMenu, '&Help')


        self.Bind(wx.EVT_MENU, self.OnOpenCardManager, id=ID_CARDS_CARD_MANAGER)
        self.Bind(wx.EVT_MENU, self.OnOpenCardBrowser, id=ID_CARDS_CARD_BROWSER)
        self.Bind(wx.EVT_MENU, self.OnEditTestCard, id=ID_CARDS_EDIT_TEST_CARD)
        self.Bind(wx.EVT_MENU, self.OnOpenChapterManager, id=ID_CARDS_CHAPTER_MANAGER)
        self.Bind(wx.EVT_MENU, self.OnOpenLearningManager, 
                  id=ID_LEARNING_LEARNING_MANAGER)
        self.Bind(wx.EVT_MENU, self.OnOpenBoxManager, 
                  id=ID_LEARNING_BOX_MANAGER)
        self.Bind(wx.EVT_MENU, self.OnRandomizePool,
                  id=ID_LEARNING_RANDOMIZE)
        self.Bind(wx.EVT_MENU, self.OnViewChapterHtml, 
                  id=ID_TOOLS_VIEW_CH_HTML)
        self.Bind(wx.EVT_MENU, self.OnViewAns, 
                  id=ID_TOOLS_VIEW_ANS)
        self.Bind(wx.EVT_MENU, self.OnDispData, 
                  id=ID_TOOLS_DISP_DATA)
        self.Bind(wx.EVT_MENU, self.OnContents, id=ID_HELP_CONTENTS)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=ID_HELP_ABOUT)

        self.SetMenuBar(MenuBar)

    def EnableDataMenu(self):
        self.FileMenu.Enable(ID_FILE_CLOSE, True)
        self.FileMenu.Enable(ID_FILE_SAVE, True)
        self.FileMenu.Enable(ID_FILE_SAVE_AS, True)
        self.FileMenu.Enable(ID_FILE_IMPORT, True)
        self.FileMenu.Enable(ID_FILE_EXPORT, True)

        self.CardsMenu.Enable(ID_CARDS_CARD_MANAGER, True)
        self.CardsMenu.Enable(ID_CARDS_CARD_BROWSER, True)
        self.CardsMenu.Enable(ID_CARDS_EDIT_TEST_CARD, True)
        self.CardsMenu.Enable(ID_CARDS_CHAPTER_MANAGER, True)
        self.LearningMenu.Enable(ID_LEARNING_LEARNING_MANAGER, True)
        self.LearningMenu.Enable(ID_LEARNING_BOX_MANAGER, True)
        self.LearningMenu.Enable(ID_LEARNING_RANDOMIZE, True)
        self.ToolsMenu.Enable(ID_TOOLS_VIEW_CH_HTML, True)
        self.ToolsMenu.Enable(ID_TOOLS_VIEW_ANS, True)
        self.ToolsMenu.Enable(ID_TOOLS_DISP_DATA, True)

    def DisableDataMenu(self):
        self.FileMenu.Enable(ID_FILE_CLOSE, False)
        self.FileMenu.Enable(ID_FILE_SAVE, False)
        self.FileMenu.Enable(ID_FILE_SAVE_AS, False)
        self.FileMenu.Enable(ID_FILE_IMPORT, False)
        self.FileMenu.Enable(ID_FILE_EXPORT, False) 
        self.CardsMenu.Enable(ID_CARDS_CARD_MANAGER, False)
        self.CardsMenu.Enable(ID_CARDS_CARD_BROWSER, False)
        self.CardsMenu.Enable(ID_CARDS_EDIT_TEST_CARD, False)
        self.CardsMenu.Enable(ID_CARDS_CHAPTER_MANAGER, False)
        self.LearningMenu.Enable(ID_LEARNING_LEARNING_MANAGER, False)
        self.LearningMenu.Enable(ID_LEARNING_BOX_MANAGER, False)
        self.LearningMenu.Enable(ID_LEARNING_RANDOMIZE, False)
        self.ToolsMenu.Enable(ID_TOOLS_VIEW_CH_HTML, False)
        self.ToolsMenu.Enable(ID_TOOLS_VIEW_ANS, False)
        self.ToolsMenu.Enable(ID_TOOLS_DISP_DATA, False)

    def Save(self):
        if self.filename:
            self.CardSet.Save(self.filename)
        else:
            dir = self.Config.get('directories', 'card_dir')
            dlg = wx.FileDialog(self, message='Save as ...', defaultDir = dir, 
                        defaultFile='', wildcard=wildcard, style=wx.SAVE)

            if dlg.ShowModal() == wx.ID_OK:
                filename =  dlg.GetPaths()[0]

                # On Linux we need to make sure that the extension is added
                # On windows the dialog adds the extension automatically
                root, ext = os.path.splitext(filename)
                if ext == '':
                    filename = root+'.%s' % defext


                print('Save: ', filename)

                if os.path.exists(filename):
                    msg = wx.MessageDialog(self, "File already exists. Are you sure you want to overwrite it?", "Warning",
                                wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_QUESTION)
                    ans = msg.ShowModal()
                    if ans == wx.ID_YES:
                        self.filename = filename
                        self.CardSet.Save(self.filename)

                        # Update config
                        self.Config.set('directories', 'card_dir', os.path.dirname(filename))
                    elif ans == wx.ID_NO:
                        self.Save() 
                    elif ans == wx.ID_CANCEL:
                        pass
                    else:
                        print("Invalid ID")

                    msg.Destroy()
                else:
                    self.filename = filename
                    self.CardSet.Save(self.filename)
                    # Update config
                    self.Config.set('directories', 'card_dir', os.path.dirname(filename))

            dlg.Destroy()

    def SaveAs(self):
        dir = self.Config.get('directories', 'card_dir')
        dlg = wx.FileDialog(self, message='Save as ...', defaultDir = dir, 
                    defaultFile='', wildcard=wildcard, style=wx.SAVE)

        if dlg.ShowModal() == wx.ID_OK:
            filename =  dlg.GetPaths()[0]

            if os.path.exists(filename):
                msg = wx.MessageDialog(self, "File already exists. Are you sure you want to overwrite it?",
                                       "Warning",
                            wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_QUESTION)
                ans = msg.ShowModal()
                if ans == wx.ID_YES:
                    self.filename = filename
                    self.CardSet.Save(self.filename)

                    # Update config
                    self.Config.set('directories', 'card_dir', os.path.dirname(filename))
                elif ans == wx.ID_NO:
                    self.SaveAs() 
                elif ans == wx.ID_CANCEL:
                    pass
                else:
                    print("Invalid ID")

                msg.Destroy()
            else:
                self.filename = filename
                self.CardSet.Save(self.filename)
                # Update config
                self.Config.set('directories', 'card_dir', os.path.dirname(filename))

        dlg.Destroy()

    def AddFileToHistory(self):
        if self.filename != '':
            self.FileHistory.AddFileToHistory(self.filename)

    def SaveFileHistory(self):
        files = ''
        for i in range(self.FileHistory.GetCount()):
            if i == 0:
                files = self.FileHistory.GetHistoryFile(i)
            else:
                files += ','
                files += self.FileHistory.GetHistoryFile(i)

        self.Config.set('file_history', 'files', files)

    def LoadFileHistory(self):
        try:
            files = self.Config.get('file_history', 'files')
            if files != '':
                files = files.split(',')
                files.reverse()
                for f in files:
                    self.FileHistory.AddFileToHistory(f)
        except:
            return

    def OnNew(self, event):
        if self.CardSet:
            if self.CardSet.IsSaved():
                self.MakeNewTestSet()
            else:
                dlg = wx.MessageDialog(self, "Active set not saved.  Do you want to save it?", "Warning",
                                wx.YES_NO | wx.YES_DEFAULT | wx.CANCEL | wx.ICON_QUESTION)
                ans = dlg.ShowModal()
                if ans == wx.ID_YES:
                    self.Save()
                    self.AddFileToHistory()
                    self.MakeNewTestSet()
                elif ans == wx.ID_NO:
                    self.AddFileToHistory()
                    self.MakeNewTestSet()
                elif ans == wx.ID_CANCEL:
                    pass

                dlg.Destroy()
        else:
            self.MakeNewTestSet()
            self.TestPanel.Show(True)
            self.Layout()

            self.EnableDataMenu()

        self.GenerateTitle()

    def MakeNewTestSet(self):
        if self.CardSet:
            self.CardSet.Close()
        self.CardSet = FlashCard.FlashCardSet()
        self.TestPanel.SetCardSet(self.CardSet)
        self.TestPanel.StartTest()
        self.filename = None

    def OnSave(self, event):
        self.Save()
        self.GenerateTitle()

    def OnSaveAs(self, event):
        self.SaveAs()
        self.GenerateTitle()
        
    def OnOpen(self, event):
        dir = self.Config.get('directories', 'card_dir')

        if not self.CardSet:
            dlg = wx.FileDialog(self, message='Choose a file', defaultDir = dir, 
                        defaultFile='', wildcard=wildcard, style=wx.OPEN)

            if dlg.ShowModal() == wx.ID_OK:
                filename = dlg.GetPaths()[0]
                self.Open(filename)
                
        else:
            if not self.CardSet.IsSaved():
                dlg = wx.MessageDialog(self, "Active set not saved.  Do you want to save it.", "Warning",
                                wx.YES_NO | wx.YES_DEFAULT | wx.CANCEL | wx.ICON_QUESTION)
                ans = dlg.ShowModal()
                if ans == wx.ID_YES:
                    self.Save()
                    self.AddFileToHistory()
                elif ans == wx.ID_NO:
                    self.AddFileToHistory()
                elif ans == wx.ID_CANCEL:
                    dlg.Destroy()
                    return

                dlg.Destroy()

            dlg = wx.FileDialog(self, message='Choose a file', defaultDir = dir, 
                        defaultFile='', wildcard=wildcard, style=wx.OPEN)

            if dlg.ShowModal() == wx.ID_OK:
                filename = dlg.GetPaths()[0]
                self.LoadCardSet(filename)

        self.GenerateTitle()
    
    def Open(self, filename):
        self.filename = filename
        self.CardSet = FlashCard.FlashCardSet()
        self.CardSet.Load(self.filename)
        self.TestPanel.SetCardSet(self.CardSet)
        self.TestPanel.Show(True)
        self.TestPanel.StartTest()
        self.Layout()
        # Update configuration
        self.Config.set('directories', 'card_dir', os.path.dirname(filename))

        self.EnableDataMenu()

    def CloseCardSet(self):
        self.CardSet.Close()
        self.CardSet = None
        self.filename = None
        self.TestPanel.Show(False)

    def SaveAndCloseCardSet(self):
        ans = wx.ID_YES
        if self.CardSet.IsSaved():
            self.CloseCardSet()
        else:
            dlg = wx.MessageDialog(self, "Active set not saved.  Do you want to save it?", "Warning",
                            wx.YES_NO | wx.YES_DEFAULT | wx.CANCEL | wx.ICON_QUESTION)
            ans = dlg.ShowModal()
            if ans == wx.ID_YES:
                self.Save()
                self.AddFileToHistory()
                self.CloseCardSet()
            elif ans == wx.ID_NO:
                self.AddFileToHistory()
                self.CloseCardSet()
            elif ans == wx.ID_CANCEL:
                pass

            dlg.Destroy()

        return ans

    def OnFileHistory(self, event):
        # get the file based on the menu ID
        fileNum = event.GetId() - wx.ID_FILE1
        filename = self.FileHistory.GetHistoryFile(fileNum)

        # now open the file
        if not self.CardSet:
            self.Open(filename)
                
        else:
            if not self.CardSet.IsSaved():
                dlg = wx.MessageDialog(self, "Active set not saved.  Do you want to save it.", "Warning",
                                wx.YES_NO | wx.YES_DEFAULT | wx.CANCEL | wx.ICON_QUESTION)
                ans = dlg.ShowModal()
                if ans == wx.ID_YES:
                    self.Save()
                    self.AddFileToHistory()
                elif ans == wx.ID_NO:
                    self.AddFileToHistory()
                elif ans == wx.ID_CANCEL:
                    dlg.Destroy()
                    return

                dlg.Destroy()

                self.LoadCardSet(filename)

        self.GenerateTitle()

    def OnClose(self, event):
        self.SaveAndCloseCardSet()
        self.DisableDataMenu()
        self.GenerateTitle()

    def OnImportWizard(self, event):
        if not self.CardSet:
            return

        if self.CardSet.GetChapterCount() == 0:
            dlg = wx.MessageDialog(self, "Add some chapters first", "Error", wx.OK | wx.ICON_ERROR)
            dlg.CenterOnParent(wx.BOTH)
            dlg.ShowModal()
            dlg.Destroy()
            return

        iconfile = os.path.join(self.runtimepath, 'icons/pyFlashCards2-import.png')
        bitmap = wx.Bitmap(iconfile, wx.BITMAP_TYPE_PNG)
        wizard = wx.adv.Wizard(self, -1, "Import Wizard", bitmap)
        page1 = iw.ImportTypePage(wizard, FlashCard.ImportTypeList)
        page2 = iw.FilePage(wizard, self.Config.get('directories', 'import_dir'), FlashCard.ImportWildcard)
        page3 = iw.ChapterPage(wizard, self.CardSet.GetChapters())
        wx.adv.WizardPageSimple.Chain(page1, page2)
        wx.adv.WizardPageSimple.Chain(page2, page3)

        if wizard.RunWizard(page1):
            ImportType = page1.GetData()
            ImportFile = page2.GetData()
            ImportChapter = page3.GetData()
            if os.path.exists(ImportFile):
                self.Config.set('directories', 'import_dir', os.path.dirname(ImportFile))
                n = self.CardSet.Import(ImportType, ImportFile.encode('utf-8'), ImportChapter)
                dlg = wx.MessageDialog(self, "%d cards imported" % n, "Import result", wx.OK | wx.ICON_INFORMATION)
                dlg.ShowModal()
                dlg.Destroy()

        wizard.Destroy()

    def OnExportWizard(self, event):
        if not self.CardSet:
            return

        if self.CardSet.GetChapterCount() == 0:
            dlg = wx.MessageDialog(self, "Add some chapters first", "Error", wx.OK | wx.ICON_ERROR)
            dlg.CenterOnParent(wx.BOTH)
            dlg.ShowModal()
            dlg.Destroy()
            return

        iconfile = os.path.join(self.runtimepath, 'icons/pyFlashCards2-export.png')
        bitmap = wx.Bitmap(iconfile, wx.BITMAP_TYPE_PNG)
        wizard = wx.adv.Wizard(self, -1, "Export Wizard", bitmap)
        page1 = ew.ChapterPage(wizard, self.CardSet.GetChapters())
        page2 = ew.ExportTypePage(wizard)
        page3 = ew.FilePage(wizard, self.Config.get('directories', 'export_dir'), page2, page1)
        wx.adv.WizardPageSimple.Chain(page1, page2)
        wx.adv.WizardPageSimple.Chain(page2, page3)

        if wizard.RunWizard(page1):
            ExportChapter = page1.GetData()
            ExportType = page2.GetData()
            ExportFile = page3.GetData()
            if ExportFile:
                self.Config.set('directories', 'export_dir', os.path.dirname(ExportFile))
                n = self.CardSet.Export(ExportType, ExportFile.encode('utf-8'), ExportChapter)
                dlg = wx.MessageDialog(self, "%d cards exported" % n, "Export result", wx.OK | wx.ICON_INFORMATION)
                dlg.ShowModal()
                dlg.Destroy()
            else:
                dlg = wx.MessageDialog(self, "You must select a file", "Export result", wx.OK | wx.ICON_INFORMATION)
                dlg.ShowModal()
                dlg.Destroy()

        wizard.Destroy()

    def OnExit(self, event):
        self.Close()

    def OnCloseWindow(self, event):
        if self.CardSet:
            if self.SaveAndCloseCardSet() == wx.ID_CANCEL:
                return

        self.SaveFileHistory()

        self.WriteConfig()
        self.WriteAutoCorr()

        event.Skip()

    def OnSize(self, event):
        w, h = event.GetSize()

        if self.IsMaximized():
            self.Config.set('window_size', 'max', 'true')
        else:
            self.Config.set('window_size', 'max', 'false')
            self.Config.set('window_size', 'width', str(w))
            self.Config.set('window_size', 'height', str(h))

        event.Skip()

    def OnOpenCardManager(self, event):
        if not self.CardSet:
            return

        if self.CardSet.GetChapterCount() == 0:
            dlg = wx.MessageDialog(self, "Add some chapters first", "Error", wx.OK | wx.ICON_ERROR)
            dlg.CenterOnParent(wx.BOTH)
            dlg.ShowModal()
            return

        self.Hide()

        dlg = CardManagerDlg(self, self.CardSet, self.filename, self.Config, self.autocorr, self.help, self.runtimepath)
        dlg.ShowModal()
        self.CardSet, self.Config, self.autocorr = dlg.GetData()
        dlg.Destroy()

        self.Show()

        self.TestPanel.Update()

        if self.DispData:
            self.DispDataWin.Update()

    def OnOpenCardBrowser(self, event):
        if not self.CardSet:
            return

        if self.CardSet.GetChapterCount() == 0:
            dlg = wx.MessageDialog(self, "Add some chapters first", "Error", wx.OK | wx.ICON_ERROR)
            dlg.CenterOnParent(wx.BOTH)
            dlg.ShowModal()
            return

        dlg = CardBrowserDlg(self, -1, self.CardSet, self.Config)
        dlg.ShowModal()
        dlg.Destroy()

    def OnEditTestCard(self, event):
        if not self.CardSet or not self.CardSet.GetTestCard():
            return

        if self.CardSet.GetChapterCount() == 0:
            dlg = wx.MessageDialog(self, "Add some chapters first", "Error", wx.OK | wx.ICON_ERROR)
            dlg.CenterOnParent(wx.BOTH)
            dlg.ShowModal()
            return

        dlg = CardManagerDlg(self, self.CardSet, self.filename, self.Config, self.autocorr, self.help, self.runtimepath)
        dlg.SelectCard(self.CardSet.GetTestCard())
        dlg.ShowModal()
        self.CardSet, self.Config, self.autocorr = dlg.GetData()
        dlg.Destroy()

        self.TestPanel.Update()

        if self.DispData:
            self.DispDataWin.Update()

    def OnOpenChapterManager(self, event):
        dlg = ChapterManagerDlg(self, self.CardSet)
        dlg.CenterOnParent()
        dlg.ShowModal()
        self.ChapterSet = dlg.GetCardSet()
        dlg.Destroy()

        self.TestPanel.Update()

        if self.DispData:
            self.DispDataWin.Update()

    def OnOpenLearningManager(self, event):
        dlg = LearningManagerDlg(self, self.CardSet, self.help, self.runtimepath)
        dlg.ShowModal()
        self.CardSet = dlg.GetCardSet()
        dlg.Destroy()

        self.TestPanel.Update()

        if self.DispData:
            self.DispDataWin.Update()

    def OnOpenBoxManager(self, event):
        dlg = BoxManagerDlg(self, self.CardSet)
        val = dlg.ShowModal()
        if val == wx.ID_OK:
            MaxList, StudyBox = dlg.GetData()
            # MaxList has a list of tuplets with box id and the new max value
            for BoxIndex, MaxStr in MaxList:
                try:
                    max = min(10000, int(MaxStr))
                    self.CardSet.SetBoxCapacity(BoxIndex, max)
                except:
                    # Leave the box size unchanged if the new size was invalid 
                    print('Something wrong MaxStr=', MaxStr)
            self.CardSet.SetStudyBox(StudyBox)
        else:
            print('Canceled')

        dlg.Destroy()

        if self.DispData:
            self.DispDataWin.Update()

    def OnRandomizePool(self, event):
        self.CardSet.RandomizePool()
        dlg = wx.MessageDialog(self, "Pool randomized", "Info", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        
    def OnViewChapterHtml(self, event):
        if not self.CardSet or not self.CardSet.GetTestCard():
            return

        chapter = self.CardSet.GetTestCard().GetChapter()

        sp = wx.StandardPaths.Get()
        UserDataDir = sp.GetUserDataDir()
        filename = os.path.join(UserDataDir, chapter+'.html')

        self.CardSet.ExportHTML(filename, chapter)

        webbrowser.open(filename, 0)

    def OnViewAns(self, event):
        if not self.CardSet or not self.CardSet.GetTestCard():
            return

        TestCard = self.CardSet.GetTestCard()
        dlg=ViewDlg.ViewDialog(None, -1, "View Answer")
        dlg.Maximize()
        face = self.CardSet.GetBackFontFace()
        size = self.CardSet.GetBackFontSize()
        dlg.SetPage(TestCard.GetBackHtml(face, size))
        dlg.ShowModal()
        dlg.Destroy()

    def OnDispData(self, event):
        if self.DispData:
            return

        self.DispData = True

        self.DispDataWin = FlashCardDataDisp.FlashCardDataDispFrame(self, -1,
                                                                self.CardSet)

        self.Bind(events.EVT_WINDOW_CLOSED, self.OnDispDataClosed, 
                  self.DispDataWin)

        self.DispDataWin.Show()

    def OnDispDataClosed(self, event):
        self.DispData = False

    def OnTestPanelDataChanged(self, event):
        if self.DispData:
            self.DispDataWin.Update()

    def OnContents(self, event):
        help.DisplayContents()

    def OnAbout(self, event):
        dlg = AboutDlg.AboutDlg(self)
        dlg.ShowModal()

    #-----------------------------------------------------------------------------------
    # The functions below are utilities functions to help develop the program.  They
    # have no use in publicly released software.  They all start with Util
    #-----------------------------------------------------------------------------------
    def UtilOpenTestFile(self):
        self.filename = os.path.join(self.runtimepath, 'test/file1.ofc')
        self.CardSet = FlashCard.FlashCardSet()
        self.CardSet.Load(self.filename)
        self.TestPanel.SetCardSet(self.CardSet)
        self.TestPanel.Show(True)
        self.TestPanel.StartTest()
        self.Layout()
        
        self.EnableDataMenu()

class TestPanel(wx.Panel):
    def __init__(self, parent, id, CardSet):
        wx.Panel.__init__(self, parent, id, name='TestPanel')

        self.GenerateFontList()

        self.CardSet = CardSet
        self.State = ID_TEST_PANEL_STATE_SHOW_NONE

        sizer = wx.BoxSizer(wx.VERTICAL)

        # New line in the GUI
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.BoxDisp = wx.StaticText(self, 1, "Box")
        f = self.BoxDisp.GetFont()
        f.SetPointSize(12)
        self.BoxDisp.SetFont(f)
        
        sizer1.Add(self.BoxDisp, 0)

        sizer.Add(sizer1, 0, wx.CENTER)

        # New line in the GUI
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.ChapterDisp = wx.StaticText(self, 1, "Chapter")
        f = self.ChapterDisp.GetFont()
        f.SetPointSize(12)
        self.ChapterDisp.SetFont(f)
        
        sizer1.Add(self.ChapterDisp, 0)

        sizer.Add(sizer1, 0, wx.CENTER)

        # New line in the GUI
        splitter = wx.SplitterWindow(self, -1)

        self.FrontDisp = html.HtmlWindow(splitter, -1, style=wx.SUNKEN_BORDER | wx.HSCROLL)
        self.BackDisp = html.HtmlWindow(splitter, -1, style=wx.SUNKEN_BORDER | wx.HSCROLL)
        
        #splitter.SplitHorizontally(self.FrontDisp, self.BackDisp, 0)
        splitter.SplitVertically(self.FrontDisp, self.BackDisp, 0)
        splitter.SetMinimumPaneSize(20)

        sizer.Add(splitter, 1, wx.EXPAND)

        # New line in the GUI
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)

        sizer11 = wx.BoxSizer(wx.VERTICAL)
        sizer111 = wx.BoxSizer(wx.HORIZONTAL)
        self.FrontFontLabel = wx.StaticText(self, -1, 'Front font:')
        sizer111.Add(self.FrontFontLabel, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.FrontFontFaceChoice = wx.Choice(self, ID_TP_FRONT_FONT_FACE, 
                                              choices=self.FontList)
        sizer111.Add(self.FrontFontFaceChoice, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.FrontSizeLabel = wx.StaticText(self, -1, 'Size: ')
        sizer111.Add(self.FrontSizeLabel, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.FrontFontSizeChoice = wx.Choice(self, ID_TP_FRONT_FONT_SIZE,
                                              choices=self.FontSizeList)
        sizer111.Add(self.FrontFontSizeChoice, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        #self.FrontDisp = html.HtmlWindow(self, -1, style=wx.SUNKEN_BORDER | wx.HSCROLL)

        if display_mode == mode_mini:
            self.FrontFontSizeChoice.Hide()
            self.FrontFontFaceChoice.Hide()
            self.FrontFontLabel.Hide()
            self.FrontSizeLabel.Hide()

        if display_mode != mode_mini:
            sizer11.Add(sizer111, 0)
        #sizer11.Add(self.FrontDisp, 1, wx.EXPAND)
        sizer1.Add(sizer11, 1, wx.EXPAND)

        sizer11 = wx.BoxSizer(wx.VERTICAL)
        sizer111 = wx.BoxSizer(wx.HORIZONTAL)
        self.BackFontLabel = wx.StaticText(self, -1, 'Back font: ')
        sizer111.Add(self.BackFontLabel, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.BackFontFaceChoice = wx.Choice(self, ID_TP_BACK_FONT_FACE, 
                                              choices=self.FontList)
        sizer111.Add(self.BackFontFaceChoice, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.BackSizeLabel = wx.StaticText(self, -1, 'Size: ')
        sizer111.Add(self.BackSizeLabel, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.BackFontSizeChoice = wx.Choice(self, ID_TP_BACK_FONT_SIZE,
                                              choices=self.FontSizeList)
        sizer111.Add(self.BackFontSizeChoice, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        #self.BackDisp = html.HtmlWindow(self, -1, style=wx.SUNKEN_BORDER | wx.HSCROLL)

        if display_mode == mode_mini:
            self.BackFontSizeChoice.Hide()
            self.BackFontFaceChoice.Hide()
            self.BackFontLabel.Hide()
            self.BackSizeLabel.Hide()

        if display_mode != mode_mini:
            sizer11.Add(sizer111, 0)
        #sizer11.Add(self.BackDisp, 1, wx.EXPAND)
        sizer1.Add(sizer11, 1, wx.EXPAND)

        #sizer.Add(sizer1, 1, wx.EXPAND)
        sizer.Add(sizer1, 0, wx.EXPAND)

        # New line in the GUI
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.ShowAnswerButton = wx.Button(self, ID_LEARN_SHOW_ANSWER,
                                          'Show answer')
        self.KnowButton = wx.Button(self, ID_LEARN_KNOW, "Know")
        self.NotKnowButton = wx.Button(self, ID_LEARN_NOT_KNOW, "Don't know")
        self.NotAgainButton = wx.Button(self, ID_LEARN_NOT_AGAIN, "Don't ask again")
        self.HideAnswerButton = wx.Button(self, ID_LEARN_HIDE_ANSWER,
                                          'Hide answer')
        self.ShowAnswerButton.Disable()
        self.KnowButton.Show(False)
        self.NotKnowButton.Show(False)
        self.NotAgainButton.Show(False)
        self.HideAnswerButton.Show(False)

        self.Bind(wx.EVT_BUTTON, self.OnShowAnswer, self.ShowAnswerButton)
        self.Bind(wx.EVT_BUTTON, self.OnKnow, self.KnowButton)
        self.Bind(wx.EVT_BUTTON, self.OnNotKnow, self.NotKnowButton)
        self.Bind(wx.EVT_BUTTON, self.OnNotAgain, self.NotAgainButton)
        self.Bind(wx.EVT_BUTTON, self.OnHideAnswer, self.HideAnswerButton)

        sizer1.Add(self.ShowAnswerButton)
        sizer1.Add(self.KnowButton)
        sizer1.Add(self.NotKnowButton)
        sizer1.Add(self.NotAgainButton)
        sizer1.Add(self.HideAnswerButton)

        sizer.Add(sizer1, 0, wx.CENTER | wx.BOTTOM, 10)
        
        self.SetAutoLayout(True)
        self.SetSizerAndFit(sizer)

        # Bind events
        self.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_CHAR, self.OnChar)
        self.FrontFontFaceChoice.Bind(wx.EVT_CHOICE, self.OnFrontFontFaceChoice,
                id=ID_TP_FRONT_FONT_FACE)
        self.FrontFontSizeChoice.Bind(wx.EVT_CHOICE, self.OnFrontFontSizeChoice,
                id=ID_TP_FRONT_FONT_SIZE)
        self.BackFontFaceChoice.Bind(wx.EVT_CHOICE, self.OnBackFontFaceChoice,
                id=ID_TP_BACK_FONT_FACE)
        self.BackFontSizeChoice.Bind(wx.EVT_CHOICE, self.OnBackFontSizeChoice,
                id=ID_TP_BACK_FONT_SIZE)

    def GenerateFontList(self):
        fe = wx.FontEnumerator()
        fe.EnumerateFacenames()
        self.FontList = fe.GetFacenames()
        self.FontList.sort()
        self.FontList[:0]=[u'Default']

        # This works on windows, but not on Linux
        # self.FontSizeList = range(8)

        self.FontSizeList = []
        for i in range(8):
            self.FontSizeList.append(str(i))


    def UpdateFrontDisp(self):
        face = self.CardSet.GetFrontFontFace()
        size = self.CardSet.GetFrontFontSize()
        self.FrontDisp.SetPage(self.TestCard.GetFrontHtml(face, size))

    def UpdateBackDisp(self):
        face = self.CardSet.GetBackFontFace()
        size = self.CardSet.GetBackFontSize()
        self.BackDisp.SetPage(self.TestCard.GetBackHtml(face, size))

    def Update(self):
        if self.State == ID_TEST_PANEL_STATE_SHOW_NONE:
            self.TestCard = self.CardSet.NextTestCard() 
            if self.TestCard == None:
                return

            self.UpdateFrontDisp()
            self.BoxDisp.SetLabel('Box %d' % self.TestCard.GetBox())
            self.ChapterDisp.SetLabel('Chapter: %s' % self.TestCard.GetChapter())
            self.ShowAnswerButton.Enable()
            self.State = ID_TEST_PANEL_STATE_SHOW_QUESTION

        elif self.State == ID_TEST_PANEL_STATE_SHOW_QUESTION:
            # Check if the test card was removed
            self.TestCard = self.CardSet.GetTestCard()
            if self.TestCard == None:
                # If yes, try to get a new card     
                self.TestCard = self.CardSet.NextTestCard()
                if self.TestCard == None:
                    # If now new card is available update the display
                    self.FrontDisp.SetPage(EmptyHtml)
                    self.BackDisp.SetPage(EmptyHtml)
                    self.ShowAnswerButton.Disable()
                    self.State = ID_TEST_PANEL_STATE_SHOW_NONE
                else:
                    # Otherwise, show the new card 
                    self.UpdateFrontDisp()
                    self.BoxDisp.SetLabel('Box %d' % self.TestCard.GetBox())
                    self.ChapterDisp.SetLabel('Chapter: %s' % self.TestCard.GetChapter())
            else:
                # If not, update the display in case the text changed
                self.UpdateFrontDisp()
                self.BoxDisp.SetLabel('Box %d' % self.TestCard.GetBox())
                self.ChapterDisp.SetLabel('Chapter: %s' % self.TestCard.GetChapter())

        elif self.State == ID_TEST_PANEL_STATE_SHOW_ANSWER:
            # Check if the test card was removed
            self.TestCard = self.CardSet.GetTestCard()
            if self.TestCard == None:
                # If yes, try to get a new card     
                self.TestCard = self.CardSet.NextTestCard()
                if self.TestCard == None:
                    # If now new card is available update the display
                    self.FrontDisp.SetPage('')
                    self.BackDisp.SetPage('')
                    self.HideKnowButtons()
                    self.ShowAnswerButton.Show(True)
                    self.ShowAnswerButton.Disable()
                    self.Layout()
                    self.State = ID_TEST_PANEL_STATE_SHOW_NONE
                else:
                    # Otherwise, show the new card 
                    self.UpdateFrontDisp()
                    self.BackDisp.SetPage('')
                    self.BoxDisp.SetLabel('Box %d' % self.TestCard.GetBox())
                    self.ChapterDisp.SetLabel('Chapter: %s' % self.TestCard.GetChapter())
                    self.HideKnowButtons()
                    self.ShowAnswerButton.Show(True)
                    self.ShowAnswerButton.Enable()
                    self.Layout()
                    self.State = ID_TEST_PANEL_STATE_SHOW_QUESTION
            else:
                # If not, update the display in case the text changed
                self.UpdateFrontDisp()
                self.UpdateBackDisp()
                self.BoxDisp.SetLabel('Box %d' % self.TestCard.GetBox())
                self.ChapterDisp.SetLabel('Chapter: %s' % self.TestCard.GetChapter())

        self.SetFocusIgnoringChildren()
            

    def StartTest(self):
        self.FrontDisp.SetPage('')
        self.BackDisp.SetPage('')

        # Update display of fonts and size
        self.UpdateFontDisp()

        self.TestCard = self.CardSet.NextTestCard()

        if self.TestCard == None:
            self.ShowAnswerButton.Enable(False)
            self.BoxDisp.SetLabel('Box')
            self.ChapterDisp.SetLabel('Chapter')
            self.Layout()
            self.State = ID_TEST_PANEL_STATE_SHOW_NONE
            return

        self.UpdateFrontDisp()
        self.BoxDisp.SetLabel('Box %d' % self.TestCard.GetBox())
        self.ChapterDisp.SetLabel('Chapter: %s' % self.TestCard.GetChapter())
        self.ShowAnswerButton.Show(True)
        self.HideKnowButtons()
        self.ShowAnswerButton.Enable()
        self.SetFocusIgnoringChildren()

        self.Layout()

        self.State = ID_TEST_PANEL_STATE_SHOW_QUESTION

    def UpdateFontDisp(self):
        face = self.CardSet.GetFrontFontFace()
        if face and face in self.FontList:
            self.FrontFontFaceChoice.SetStringSelection(face)
        else:
            self.FrontFontFaceChoice.SetSelection(0)

        size = str(self.CardSet.GetFrontFontSize())  # Changed from backticks to str()
        if size in self.FontSizeList:
            self.FrontFontSizeChoice.SetStringSelection(size)

        face = self.CardSet.GetBackFontFace()
        if face and face in self.FontList:
            self.BackFontFaceChoice.SetStringSelection(face)
        else:
            self.BackFontFaceChoice.SetSelection(0)

        size = str(self.CardSet.GetBackFontSize())  # Changed from backticks to str()
        if size in self.FontSizeList:
            self.BackFontSizeChoice.SetStringSelection(size)


    def ShowAnswer(self):
        if self.TestCard == None:
            return

        self.UpdateBackDisp()

        self.ShowKnowButtons()
        self.ShowAnswerButton.Show(False)
        self.Layout()
        self.SetFocusIgnoringChildren()

        self.State = ID_TEST_PANEL_STATE_SHOW_ANSWER

    def OnShowAnswer(self, event):
        self.ShowAnswer()

    def Know(self):
        self.CardSet.PromoteTestCard()
        self.TestCard = self.CardSet.NextTestCard()

        if self.TestCard == None:
            return

        self.UpdateFrontDisp()
        self.BackDisp.SetPage('')
        self.BoxDisp.SetLabel('Box %d' % self.TestCard.GetBox())
        self.ChapterDisp.SetLabel('Chapter: %s' % self.TestCard.GetChapter())
        self.HideKnowButtons()
        self.ShowAnswerButton.Show(True)
        self.Layout()
        self.SetFocusIgnoringChildren()

        self.State = ID_TEST_PANEL_STATE_SHOW_QUESTION

        evt = TestPanelEvent(myEVT_LP_DATA_CHANGED, self.GetId())
        self.GetEventHandler().ProcessEvent(evt)

    def OnKnow(self, event):
        self.Know()

    def NotKnow(self):
        self.CardSet.DemoteTestCard()
        self.TestCard = self.CardSet.NextTestCard()

        if self.TestCard == None:
            return

        self.UpdateFrontDisp()
        self.BackDisp.SetPage('')
        self.BoxDisp.SetLabel('Box %d' % self.TestCard.GetBox())
        self.ChapterDisp.SetLabel('Chapter: %s' % self.TestCard.GetChapter())
        self.HideKnowButtons()
        self.ShowAnswerButton.Show(True)
        self.Layout()
        self.SetFocusIgnoringChildren()

        self.State = ID_TEST_PANEL_STATE_SHOW_QUESTION

        evt = TestPanelEvent(myEVT_LP_DATA_CHANGED, self.GetId())
        self.GetEventHandler().ProcessEvent(evt)

    def OnNotKnow(self, event):
        self.NotKnow()

    def NotAgain(self):
        self.CardSet.PromoteTestCardToLastBox()
        self.TestCard = self.CardSet.NextTestCard()

        if self.TestCard == None:
            return

        self.UpdateFrontDisp()
        self.BackDisp.SetPage('')
        self.BoxDisp.SetLabel('Box %d' % self.TestCard.GetBox())
        self.ChapterDisp.SetLabel('Chapter: %s' % self.TestCard.GetChapter())
        self.HideKnowButtons()
        self.ShowAnswerButton.Show(True)
        self.Layout()
        self.SetFocusIgnoringChildren()

        self.State = ID_TEST_PANEL_STATE_SHOW_QUESTION

        evt = TestPanelEvent(myEVT_LP_DATA_CHANGED, self.GetId())
        self.GetEventHandler().ProcessEvent(evt)

    def OnNotAgain(self, event):
        self.NotAgain()

    def HideAnswer(self):
        self.BackDisp.SetPage('')
        self.HideKnowButtons()
        self.ShowAnswerButton.Show(True)
        self.Layout()
        self.SetFocusIgnoringChildren()

        self.State = ID_TEST_PANEL_STATE_SHOW_QUESTION

    def OnHideAnswer(self, event):
        self.HideAnswer()

    def HideKnowButtons(self):
        self.KnowButton.Show(False)
        self.NotKnowButton.Show(False)
        self.NotAgainButton.Show(False)
        self.HideAnswerButton.Show(False)

    def ShowKnowButtons(self):
        self.KnowButton.Show(True)
        self.NotKnowButton.Show(True)
        self.NotAgainButton.Show(True)
        self.HideAnswerButton.Show(True)
        
    def SetCardSet(self, CardSet):
        self.CardSet = CardSet

    def OnChar(self, event):
        keycode = event.GetKeyCode()
        #print 'TestPanel: OnChar %d' % keycode

        if self.State is ID_TEST_PANEL_STATE_SHOW_NONE:
            # Nothing to do
            pass
        elif self.State is ID_TEST_PANEL_STATE_SHOW_QUESTION:
            if keycode == wx.WXK_SPACE or keycode == wx.WXK_RETURN:
                self.ShowAnswer()
        elif self.State is ID_TEST_PANEL_STATE_SHOW_ANSWER:
            if  keycode <= 127:
                c = chr(keycode).upper()
            else:
                c = ''
            if c == 'Y' or c == 'K':
                self.Know()
            elif c == 'N':
                self.NotKnow()

        event.Skip()

    def OnSetFocus(self, event):
        #print 'TestPanel: Got focus'
        event.Skip()

    def OnKillFocus(self, event):
        #print 'TestPanel: Lost focus'
        #win  = event.GetWindow()
        #if win:
        #    print win.GetName()
        event.Skip()

    def OnLeftDown(self, event):
        self.SetFocusIgnoringChildren()

    def OnFrontFontFaceChoice(self, event):
        face = event.GetString()
        self.CardSet.SetFrontFontFace(face)
        self.UpdateFrontDisp()

    def OnFrontFontSizeChoice(self, event):
        size = int(event.GetString())
        self.CardSet.SetFrontFontSize(size)
        self.UpdateFrontDisp()

    def OnBackFontFaceChoice(self, event):
        face = event.GetString()
        self.CardSet.SetBackFontFace(face)
        self.UpdateBackDisp()

    def OnBackFontSizeChoice(self, event):
        size = int(event.GetString())
        self.CardSet.SetBackFontSize(size)
        self.UpdateBackDisp()

# Function checks if the user data directory exists. If it does not, it creates a new one.
def CheckUserDataDir():
    sp = wx.StandardPaths.Get()
    UserDataDir = sp.GetUserDataDir()
    if not os.path.exists(UserDataDir):
        print(f'Creating {UserDataDir}')  # Updated to Python 3 format
        os.makedirs(UserDataDir)


def GetConfigFileName():
    sp = wx.StandardPaths.Get()
    UserDataDir = sp.GetUserDataDir()
    return os.path.join(UserDataDir, ConfigFileName)

def GetAutoCorrFileName():
    sp = wx.StandardPaths.Get()
    UserDataDir = sp.GetUserDataDir()
    return os.path.join(UserDataDir, AutoCorrFileName)

if __name__ == '__main__':
    toopen = None
    if len(sys.argv) == 2:
        toopen = os.path.abspath(sys.argv[1])

    #print os.getcwd()
    app = wx.App(False) 
    wx.GetApp().SetAppName('pyFlashCards')
    CheckUserDataDir()
    # Create help manager
    wx.FileSystem.AddHandler(wx.ZipFSHandler())
    help = wx.html.HtmlHelpController()
    sp = wx.StandardPaths.Get()
    UserDataDir = sp.GetUserDataDir()
    help.SetTempDir(UserDataDir)
    help.AddBook('help/help.zip', 1)

    win = FlashCardFrame(None, ID_FLASH_CARD_FRAME, help)
    win.Show()
    #print sys.argv, len(sys.argv)
    if toopen != None:
        win.Open(toopen)
        win.GenerateTitle()
    
    app.MainLoop()
