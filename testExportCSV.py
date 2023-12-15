# testExportCSV.py
import sys
import os
import webbrowser
import FlashCard

runpath = os.getcwd()
file = os.path.join(runpath, 'test', 'usmle-path.ofc')
csvfile = os.path.join(runpath, 'tmp', 'test.csv')

set = FlashCard.FlashCardSet()

set.Load(file)

# Export one chapter
chapters = []
chapters.append(set.GetChapterName(5))
set.ExportCSV(csvfile, chapters, header=True)

# Export all chapters
# You need to implement this functionality if required. The current FlashCard class does not support exporting all chapters to CSV in one go.

set.Close()

webbrowser.open(csvfile, 0)
