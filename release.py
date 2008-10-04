#-------------------------------------------------------------------------------
# release.py
# This is a tool for creating a public release of pyFlashCards.  It is intended
# to be run only under linux.
# It will:
#   - remove *.pyc files
#   - remove flashcard.cfg files
#   - create a CVS tag for the new revision
#   - create an archive of the FlashCards directory
# Author:   Marcin Matuszkiewicz
#-------------------------------------------------------------------------------
# pyFlashCards is a multiplatform flash cards software.
# Copyright (C) 2006  Marcin Matuszkiewicz
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
#   Foundation, Inc.
#   51 Franklin Street, Fifth Floor
#   Boston
#   MA  02110-1301
#   USA.
#-------------------------------------------------------------------------------
# CVS information
# $Source: /cvsroot/pyflashcards/pyFlashCards/release.py,v $
# $Revision: 1.2 $
# $Date: 2008/10/04 22:29:44 $
# $Author: marcin $
#-------------------------------------------------------------------------------
import getopt, sys, os
import ConfigParser

from string import *

def main():
    global major, minor, build

    # parse revision file
    config = ConfigParser.ConfigParser()
    config.read('rev.cfg')
    try:
        major = int(config.get('rev', 'major'))
        minor = int(config.get('rev', 'minor'))
        build = int(config.get('rev', 'build'))
    except ConfigParser.NoSectionError, sec:
        print sec
    except ConfigParser.NoOptionError, opt:
        print opt

    rev = (major, minor, build)

    # remove *.pyc files
    print 'Removing *.pyc files'
    cmd = 'rm -rf *.pyc'
    os.system(cmd)

    # remove flashcards.cfg'
    print 'Removing flashcard.cfg'
    cmd = 'rm -rf flashcard.cfg'
    os.system(cmd)

    print 'Tagging revision %g.%g.%g' % rev
    
    cmd = 'cvs tag v%g_%g_%g' % (major, minor, build)
    pipe=os.popen4(cmd)

    
    code_dest = 'FlashCards'+'-%g.%g.%g'%rev+'.tgz'
    cmd = 'cd .. ; tar -czf %s %s' % (code_dest, 'FlashCards')
    os.system(cmd)

if __name__=='__main__':
    main()
