# testExportXML.py
import sys
import os
import webbrowser
import FlashCard

runpath = os.getcwd()
file = os.path.join(runpath, 'test', 'usmle-path.ofc')
xmlfile = os.path.join(runpath, 'tmp', 'test.xml')

set = FlashCard.FlashCardSet()

set.Load(file)

# Export one chapter
chapter = set.GetChapterName(5)
set.ExportXML(xmlfile, chapter)


set.Close()
