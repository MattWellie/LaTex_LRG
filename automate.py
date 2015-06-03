from Tkinter import *
from tkFileDialog import askopenfilename
from LrgParser import LrgParser
from GbkParser import GbkParser
from autoreader import Reader
from latex_writer import LatexWriter
from subprocess import call
import os
import time

__author__ = 'mwelland'
__version__ = 1.3
__version_date__ = '11/02/2015'
''' This module of the reference sequence writer creates the user interface.
    This is version 2, for which the individual operational components have
    been abstracted into separate modules.

    Program flow:

    - GUI is generated
        - User chooses an input file (type: LRG (XML) / GenBank
        - User chooses an amount of intronic flanking sequence (number)
        - User adds their username (which will be stored as a file attribute)
        - User clicks 'TRANSLATE'

    - The input file type is checked and the file_type variable is set
        - If the input is LRG, an LRG_Parser instance is created
        - If the input is GenBank, an GbkParser instance is created
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


def get_version():
    """
    Quick function to grab version details for final printing
    :return:
    """
    return 'Version: {0}, Version Date: {1}'.format(str(__version__), __version_date__)



def open_file():
    current = os.path.join(os.getcwd(), 'input')
    name = askopenfilename(initialdir='%s' % current)
    entry.delete(0, END)
    entry.insert(0, name)

def check_file_type(file_name):
    """ This function takes the file name which has been selected
        as input. This will identify .xml and .gk/gbk files, and
        will print an error message and exit the application if
        a file is used which does not match either of these types
    """
    if file_name[-4:] == '.xml':
        return 'lrg'
    elif file_name[-3:] == '.gb':
        return 'gbk'
    elif file_name[-4:] == '.gbk':
        return 'gbk'
    else:
        print 'This program only works for GenBank and LRG files'
        exit()

startingdir = os.getcwd()
try:
    new_folder = "lrg references - %s" % (time.strftime("%d-%m-%Y"))
    os.mkdir(new_folder)
except WindowsError:
    print "An up-to-date LRG output directory already exists;"
    print "This process does not need to be re-run"
    print "If significant file changes have been made please \ndelete the folder '%s' and re-try" % new_folder
    exit()
    
for filename in sorted(os.listdir('lrgs')):
    try:
        if filename == 'LRG_TEST.xml' or filename == 'GB_TEST.gb':
            continue
        # Files will not be stored directly in outputFiles anymore - requires overwrite check
        print 'Filename: %s' % filename
        write_as_latex = True
        print_clashes = True
        trim_flanking = True
        padding = 300
        file_type = check_file_type(filename)
        filepath = os.path.join('lrgs', filename)
        username = 'MWWA'
        dictionary = {}
        nm = ''
        parser_details = ''
        if file_type == 'gbk':
            print 'Running parser'
            gbk_reader = GbkParser(filepath, padding, trim_flanking)
            dictionary = gbk_reader.run()
            parser_details = gbk_reader.get_version
        elif file_type == 'lrg':
            print 'Running parser'
            lrg_reader = LrgParser(filepath, padding, trim_flanking)
            dictionary  = lrg_reader.run()
            parser_details = lrg_reader.get_version

        parser_details = '{0} {1} {2}'.format(file_type.upper(), 'Parser:', parser_details)
        
        os.chdir(new_folder)
        for transcript in dictionary['transcripts']:  
            print 'transcript:'
            transcript  
            
            input_reader = Reader()
            writer = LatexWriter()
            reader_details = 'Reader: ' + input_reader.get_version
            writer_details = 'Writer: ' + writer.get_version
            xml_gui_details = 'Control: ' + get_version()
            list_of_versions = [parser_details, reader_details, writer_details, xml_gui_details]
            lrg_num = filename.split('.')[0].replace('_', '\_')+'t'+str(transcript)
            input_list, nm = input_reader.run(dictionary, transcript, write_as_latex, list_of_versions, print_clashes, file_type, lrg_num, username)
            if file_type == 'gbk':
                file_name = dictionary['genename']+'_'+ nm
            else:
                file_name = dictionary['genename']+'_'+ filename.split('.')[0]+'t'+str(transcript)
            latex_file = writer.run(input_list, file_name, write_as_latex)
            if write_as_latex: call(["pdflatex", "-interaction=batchmode", latex_file])
            # Move back a level to prepare for optional other transcripts
            os.chdir(os.pardir)
            # quick sleep to allow for non-overlapping writes
            print str(transcript) + ' has been printed'

        print "Process has completed successfully"
        os.chdir(os.pardir)
    except AttributeError:
        os.chdir(startingdir)
        continue
    except AssertionError:  
        os.chdir(startingdir)
        continue
