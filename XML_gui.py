# -*- coding: utf-8 -*-
import os, sys, shutil
from Tkinter import *
from tkFileDialog import askopenfilename
from GUI_Parser import Parser
import xml.etree.ElementTree as etree
from subprocess import call

option = ''
def open_file():
    name = askopenfilename(defaultextension = '')
    #Add name to entry free text
    entry.delete(0, END)
    entry.insert(0, name)
def About():
    print '\nMatthew Welland, 8, January 2015'
    print 'This is a Python program for creating reference sequences'
    print 'To create sequences you will need a computer with LaTex installed\n'
    print 'Clicking the "Browse..." button will show you the local directory'
    print 'From here choose an LRG file you would like to create a reference for'
    print 'To identify the correct LRG, find the gene on http://www.lrg-sequence.org/LRG\n'
    print 'This program will produce a .PDF document'
    print 'This has been done to prevent any issues with later editing'
    print 'The document can be annontated by the use of highlighting\n\n'
    print 'If there are any faults during execution or output problems'
    print 'please contact matthew.welland@bwnft.nhs.uk, WMRGL, Birmingham\n'
    '''
    print '─────────▄──────────────▄'
    print '────────▌▒█───────────▄▀▒▌'
    print '────────▌▒▒▀▄───────▄▀▒▒▒▐'
    print '───────▐▄▀▒▒▀▀▀▀▄▄▄▀▒▒▒▒▒▐'
    print '─────▄▄▀▒▒▒▒▒▒▒▒▒▒▒█▒▒▄█▒▐'
    print '───▄▀▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▀██▀▒▌'
    print '──▐▒▒▒▄▄▄▒▒▒▒▒▒▒▒▒▒▒▒▒▀▄▒▒▌'
    print '──▌▒▒▐▄█▀▒▒▒▒▄▀█▄▒▒▒▒▒▒▒█▒▐'
    print '─▐▒▒▒▒▒▒▒▒▒▒▒▌██▀▒▒▒▒▒▒▒▒▀▄▌'
    print '─▌▒▀▄██▄▒▒▒▒▒▒▒▒▒▒▒░░░░▒▒▒▒▌'
    print '─▌▀▐▄█▄█▌▄▒▀▒▒▒▒▒▒░░░░░░▒▒▒▐'
    print '▐▒▀▐▀▐▀▒▒▄▄▒▄▒▒▒▒▒░░░░░░▒▒▒▒▌'
    print '▐▒▒▒▀▀▄▄▒▒▒▄▒▒▒▒▒▒░░░░░░▒▒▒▐'
    print '─▌▒▒▒▒▒▒▀▀▀▒▒▒▒▒▒▒▒░░░░▒▒▒▒▌'
    print '─▐▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▐'
    print '──▀▄▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▄▒▒▒▒▌'
    print '────▀▄▒▒▒▒▒▒▒▒▒▒▄▄▄▀▒▒▒▒▄▀'
    print '───▐▀▒▀▄▄▄▄▄▄▀▀▀▒▒▒▒▒▄▄▀'
    print '--──▐▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▀▀'
    '''
    print '\nSo gene\nSuch reference\nWow'

    #Operating instructions

#OS methods (not fixed for class)
#A fair amount of hard-coding is in place, just to ensure that output is in folders

def run_parser():
    #Files will not be stored directly in outputFiles anymore - requires overwrite check
    existingFiles = os.listdir('outputFiles')
    directory_and_file= entry.get()
    file_name = directory_and_file.split('/')[-1]
    if file_name[-4:] == '.xml':
		file_type = 'xml'
	elif file_name[-3:] == '.gb':
		file_type = 'gbk'
	elif file_name[-4:] == '.gbk':
		file_type = 'gbk'
	else:
		print 'This program only works for GenBank and LRG files'
		exit()
	padding = pad.get()
    xml_parser = Parser(file_name, padding, existingFiles, file_type)
    print 'Running parser'
    latex_file = xml_parser.run()
    os.chdir("outputFiles")
    os.mkdir(latex_file[0:-4]) # Try-catch, this folder may exist
    shutil.move(latex_file, os.path.join(latex_file[0:-4], latex_file))
    os.chdir(latex_file[0:-4])
    call(["pdflatex", "-interaction=batchmode", latex_file])
    print "Process has completed successfully"
    root.quit()
    
root = Tk()
menu = Menu(root)
root.config(menu=menu)
helpmenu = Menu(menu)
menu.add_command(label="Help", command=About)

text_in_label = Label(root, text="File name:")
text_in_label.grid(row=0, column=1, sticky = 'w')
entry = Entry(root)
entry.grid(row=0,column=2, sticky = 'w')
entry.insert(0, 'LRG_304.xml')
button = Button(root, text="Browse...", command=open_file)
button.grid(row=0, column=3)

padding_in_label = Label(root, text="Intronic padding:")
padding_in_label.grid(row=1, column=1, sticky = 'w')
pad = Entry(root)
pad.grid(row=1,column=2, sticky = 'w')
pad.insert(0, 300)

button = Button(root, text="QUIT", fg="red", command=root.quit)
button.grid(row=3, column=1)
parser= Button(root, text="Translate", fg="blue", command=run_parser)
parser.grid(row=3, column=2)

mainloop()
