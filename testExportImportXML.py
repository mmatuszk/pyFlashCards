# testExporImportXML.py
import sys
import os
import webbrowser
import FlashCard

runpath = os.getcwd()
file = os.path.join(runpath, 'test', 'usmle-path.ofc')
xmlfile = os.path.join(runpath, 'tmp', 'test.xml')
imported_xmlfile = os.path.join(runpath, 'tmp', 'imported_test.xml')
htmlfile = os.path.join(runpath, 'tmp', 'imported_test_html.html')

set = FlashCard.FlashCardSet()

# Load the original flashcard set
set.Load(file)

# Export one chapter to XML
chapter = set.GetChapterName(5)
set.ExportXML(xmlfile, chapter)

# Close the current set
set.Close()

# Create a new FlashCardSet instance for importing
imported_set = FlashCard.FlashCardSet()
# We need to generate some chapters first
imported_set.GenerateTestData()

# we will import into Chapter 1
chapter = 'USMLE Path'

# Import the previously exported XML file
imported_set.ImportXML(xmlfile, chapter)

# Export all chapters
imported_set.ExportHTMLAllChapters(htmlfile)

# Close the imported set
imported_set.Close()

webbrowser.open(htmlfile, 0)