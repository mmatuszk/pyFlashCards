import sys, os, os.path

sys.path.append('../')
import AutoCorr


runpath = os.getcwd()
filename = 'autocorr.xml'

ac = AutoCorr.AutoCorr()

#ac.GenerateTestData()
#ac.InsertItem(u"alpha-blocker", u"\u03B1-bl")
#ac.InsertItem(u"beta-blocker", u"\u03B2-bl")
#ac.PrintList()
#print
#ac.Save(filename)
ac.Load(filename)

str = 'alpha >alpha beta-blocker alpha <=\n'

print ac.FindReplace(str)
