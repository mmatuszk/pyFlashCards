# testExportHtml.py

import sys, os, os.path
import webbrowser
import FlashCard

runpath = os.getcwd()
file = os.path.join(runpath, 'test','usmle-path.ofc')
htmlfile = os.path.join(runpath, 'tmp', 'test.html')


set = FlashCard.FlashCardSet()

set.Load(file)

# Export one chapter
chapters = []
chapters.append(set.GetChapterName(5))
set.ExportHTML(htmlfile, chapters)

# Export all chapters
set.ExportHTMLAllChapters(htmlfile)


set.Close()

webbrowser.open(htmlfile, 0)
