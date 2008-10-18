import sys

sys.path.append('../')

import FlashCard

import os

set = FlashCard.FlashCardSet()

set.GenerateTestData()
set.SelectChapter(0)
set.SelectChapter(0)
set.Save('file2.ofc')
set.Load('file2.ofc')
#set.Close()
