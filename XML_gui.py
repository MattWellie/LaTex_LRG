# -*- coding: utf-8 -*-
from Tkinter import *
from tkFileDialog import askopenfilename
from LrgParser import LrgParser
from GbkParser import GbkParser
from reader import Reader
from latex_writer import LatexWriter
from subprocess import call

''' This module of the reference sequence writer creates the user interface.
    This is version 2, for which the individual operational components have
    been abstracted into separate modules.

    Program flow:

    - GUI is generated
        - User chooses an input file (type: LRG (XML) / GenBank
        - User chooses an amount of intronic flanking sequence (number)
        - User clicks 'TRANSLATE'

    - The input file type is checked and the file_type variable is set
        - If the input is LRG, an LRG_Parser instance is created
        - If the input is GenBank, an GBK_Parser instance is created
        - The appropriate Parser instance is used to read the input file
            contents into a dictionary object which is returned
        - The dictionary has the following structure:

            Dict { pad
                   filename
                   genename
                   refseqname
                   transcripts {  transcript {   protein_seq
                                                 cds_offset
                                                 exons {        exon_number {   genomic_start
                                                                                genomic_stop
                                                                                transcript_start
                                                                                transcript_stop
                                                                                sequence (with pad)

        - Use of this dictionary structure allows for use of absolute references
            to access each required part of the processed input, and allows for
            the extension of the format to include any features required later

    - The returned dictionary is passed through a Reader instance, which scans
        through the created dictionary, and creates a list of Strings which
        represent the typesetting which will be used for the final output.
    - The Reader instance has been chosen to write out in a generic format, to
        allow the dictionary contents to be used as a text output or for LaTex.
        Use of a Boolean write_as_latex variable can be used to decide whether
        the output will include LaTex headers and footers

    - The list output from the Reader instance is written to an output file using
        a writer object. Currently this is a LatexWriter instance, using standard
        printing to file.This could be replaced with a print to .txt for inspection
    - The LatexWriter Class creates an output directory which contains a reference
        to the input file name, intronic padding, the date and time. This is done
        to ensure that the output directory is unique and identifies the exact point
        in time when the output file was created
    - The LatexWriter also creates the full PDF output using a Python facilitated
        command line call. The output '.tex' file is created in the new output
        directory and is processed using pdflatex
'''

def open_file():
    name = askopenfilename(defaultextension = '')
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


def run_parser():
    # Files will not be stored directly in outputFiles anymore - requires overwrite check
    padding = pad.get()
    directory_and_file= entry.get()
    file_name = directory_and_file.split('/')[-1]
    file_type = check_file_type(file_name)
    dictionary = {}
    if file_type == 'gbk':
        print 'Running parser'
        gbk_reader = GBK_Parser(file_name, padding)
        dictionary = gbk_reader.run()
    elif file_type == 'lrg':
        print 'Running parser'
        lrg_reader = LrgParser(file_name, padding)
        dictionary = lrg_reader.run()

    print dictionary.keys()
    filename = dictionary['filename']
    for transcript in dictionary['transcripts']:
        input_reader = Reader(dictionary, transcript, True)
        input_list = input_reader.run()
        writer = LatexWriter(input_list, filename)
        latex_file = writer.run()
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
