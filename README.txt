At some point I'll work out what kind of license this should have...
It's open source anyway...

##Requirements and testing
pdflatex
tkinter (python graphics package)
Python 2.7

##What it does
This program takes an LRG file as input and creates a typeset reference sequence.
This sequence is designed to be used during sequence checking, and includes an
HGVS nomenclature naming system.
platform independent
requires outputFiles folder to be created

##Who its for

##How to operate it
python XML_gui.py
this command will bring up the main interface, offering two entry boxes. The top 
text entry box defaults to LRG_304 (EGFR LRG file) and can either be edited 
directly or by using the 'Browse...' button. this will show the local directory
and allow file selection directly.

There is a 'Help' button on the ribbon which will print a brief guide statement
to the command line. This can be edited in the XML_gui.py file

##Issue Tracker
stumbles on exons numbered with letters (e.g. 14a)
    - Due to a failed sorting mechanism, otherwise works

happy hunting
