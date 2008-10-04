import FlashCard

set = FlashCard.FlashCardSet()
set.Load('test1.mfc')
chapter = set.GetChapters()
set.ExportHTML('test.html', chapter[0])
