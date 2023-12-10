# testExportImportCSV.py
import sys
import os
import webbrowser
import FlashCard

runpath = os.getcwd()
file = os.path.join(runpath, 'test', 'usmle-path.ofc')
csvfile = os.path.join(runpath, 'tmp', 'test.csv')
imported_csvfile = os.path.join(runpath, 'tmp', 'imported_test.csv')
htmlfile = os.path.join(runpath, 'tmp', 'imported_test_html.html')

set = FlashCard.FlashCardSet()

# Load the original flashcard set
set.Load(file)

# Export one chapter to CSV
chapter = set.GetChapterName(5)
# Assuming the column mapping for your CSV format
colmap = {
    'front': 0,
    'front image': 1,
    'back': 2,
    'back image': 3,
    'chapter': 4  # Assuming no chapter column in the exported CSV
}
# set.ExportCSV(csvfile, chapter, header=True)
set.ExportCSVAllChapters(csvfile, header=True)

# Close the current set
set.Close()

# Create a new FlashCardSet instance for importing
imported_set = FlashCard.FlashCardSet()  
# We need to generate some chapters first
# imported_set.GenerateTestData()

# We will import into an existing chapter
chapter = 'USMLE Path'

# Import the previously exported CSV file
imported_set.ImportCSV(csvfile, colmap, header=True, create_chapter=True)

# Export all chapters to HTML for review
imported_set.ExportHTMLAllChapters(htmlfile)

# Close the imported set
imported_set.Close()

# Open the exported HTML file
webbrowser.open(htmlfile, 0)
