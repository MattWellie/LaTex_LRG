# -*- coding: utf-8 -*-
import os, shutil

from Tkinter import *
from tkFileDialog import askopenfilename
from LRG_Parser import LRG_Parser
from GBK_Parser import GBK_Parser
from reader import reader
from latex_writer import LatexWriter
from subprocess import call


def open_file():
    name = askopenfilename(defaultextension = '')
    #Add name to entry free text
    entry.delete(0, END)
    entry.insert(0, name)


def about():
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

    # Operating instructions
    # A fair amount of hard-coding is in place, just to ensure that output is in folders


def run_parser():
    # Files will not be stored directly in outputFiles anymore - requires overwrite check
    padding = pad.get()
    # existing_files= os.listdir('outputFiles')
    directory_and_file= entry.get()
    file_name = directory_and_file.split('/')[-1]
    file_type = check_file_type(file_name)
    dictionary = {}
    if file_type == 'gbk':
        print 'Running parser'
        GBK_reader = GBK_Parser(file_name, padding)
        dictionary = GBK_reader.run()
    elif file_type == 'lrg':
        print 'Running parser'
        LRG_reader = LRG_Parser(file_name, padding)
        dictionary = LRG_reader.run()

    print dictionary.keys()
    filename = dictionary['filename']
    for transcript in dictionary['transcripts']:
        input_reader = reader(dictionary, transcript, True)
        input_list = input_reader.run()
        writer = LatexWriter(input_list, filename)
        latex_file, folder_name = writer.run()
        call(["pdflatex", "-interaction=batchmode", latex_file])
        print "Process has completed successfully"
        root.quit()


def check_file_type(file_name):
    ''' This function takes the file name which has been selected
        as input. This will identify .xml and .gk/gbk files, and
        will print an error message and exit the application if
        a file is used which does not match either of these types
    '''
    if file_name[-4:] == '.xml':
        return 'lrg'
    elif file_name[-3:] == '.gb':
        return 'gbk'
    elif file_name[-4:] == '.gbk':
        return 'gbk'
    else:
        print 'This program only works for GenBank and LRG files'
        exit()


root = Tk()
menu = Menu(root)
root.config(menu=menu)
helpmenu = Menu(menu)
menu.add_command(label="Help", command=about)

text_in_label = Label(root, text="File name:")
text_in_label.grid(row=0, column=1, sticky = 'w')
entry = Entry(root)
entry.grid(row=0,column=2, sticky = 'w')
entry.insert(0, 'ASL_Genbank.gb')
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
