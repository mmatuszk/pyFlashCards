"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup
#from distutils.core import setup

APP = ['pyFlashCards.py']
DATA_FILES = [  ('icons', ['icons/pyFlashCards2-32x32.ico',
                    'icons/pyFlashCards2.png',
                    'icons/pyFlashCards2-import.png',
                    'icons/pyFlashCards2-export.png',
                    'icons/noimage.jpg']),
                ('icons/tango/16x16/actions', [ 'icons/tango/16x16/actions/document-new.png',
                    'icons/tango/16x16/actions/document-open.png',
                    'icons/tango/16x16/actions/document-save.png',
                    'icons/tango/16x16/actions/document-save-as.png',
                    'icons/tango/16x16/actions/go-next.png',
                    'icons/tango/16x16/actions/go-previous.png',
                    'icons/tango/16x16/actions/format-text-bold.png',
                    'icons/tango/16x16/actions/format-text-italic.png',
                    'icons/tango/16x16/actions/format-text-underline.png']),
                ('icons/tango/32x32/actions', [ 'icons/tango/32x32/actions/document-new.png',
                    'icons/tango/32x32/actions/document-open.png',
                    'icons/tango/32x32/actions/document-save.png',
                    'icons/tango/32x32/actions/document-save-as.png',
                    'icons/tango/32x32/actions/go-next.png',
                    'icons/tango/32x32/actions/go-previous.png',
                    'icons/tango/32x32/actions/format-text-bold.png',
                    'icons/tango/32x32/actions/format-text-italic.png',
                    'icons/tango/32x32/actions/format-text-underline.png']),
                ('autocorr', ['autocorr/autocorr.xml'])]
OPTIONS = {'argv_emulation': True, 'iconfile': 'icons/pyFlashCards2-32x32.icns'}

setup(
    name='pyFlashCards',
    version='0.4.0',
    app=APP,
    author='Marcin Matuszkiewicz',
    author_email='marcin@jewelmirror.com',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
