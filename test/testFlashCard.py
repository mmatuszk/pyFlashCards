import sys, os, os.path

sys.path.append('../')
import FlashCard

runpath = os.getcwd()
file = os.path.join(runpath, 'file2.ofc')

set = FlashCard.FlashCardSet()

set.GenerateTestData()
set.SelectChapter(0)
set.SelectChapter(0)
set.Save(file)
set.Load(file)
set.Close()
