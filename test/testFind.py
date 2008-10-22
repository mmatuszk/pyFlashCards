import sys, os, os.path

sys.path.append('../')
import FlashCard

set = FlashCard.FlashCardSet()

set.GenerateTestData()
ch = set.GetChapterName(0)
print ch

# Test forward searching
i = set.FindFirstStr(ch, 'Front1')
print i

while i >=0:
    i = set.FindNextStr(ch, i, 'Front1')
    print i

# Test backward searching
i = set.GetChapterCardCount(ch)-1
print "Searching backwards, sarting at", i
while i >=0:
    i = set.FindNextStr(ch, i, 'Back', direction=-1)
    print i
