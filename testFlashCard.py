import FlashCard

import os

set = FlashCard.FlashCardSet()

set.GenerateTestData()
set.SelectChapter(0)
set.SelectChapter(0)
set.Save('file1.mfc')
set.Load('file1.mfc')
