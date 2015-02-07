import os
import time

__author__ = 'mwelland'
""" This will be a class to receive a list of objects and a file name
    and compose the output to be written to file
    This will also check if an existing file has the same name and file
    location as the intended output file, and offer to cancel the write
    process or to delete the existing file contents to make way for new
    output
"""


class LatexWriter:

    def __init__(self, input_list, filename):

        self.input_list = input_list
        self.filename = filename
        self.latex_name = self.filename+'.tex'
        out = open(self.latex_name, "w")

    def run(self):

        os.chdir("outputFiles")
        # The folder to store the LaTex output will use the date and time to ensure unique
        folder_name = self.filename+'_'+time.strftime("%d-%m-%Y")+'_'+time.strftime("%H-%M-%S")
        os.mkdir(folder_name)
        os.chdir(folder_name)
        out = open(self.latex_name, "w")
        self.fill_output_file(out)
        return self.latex_name

    def fill_output_file(self, out):

        for line in self.input_list:
            print >> out, line
        print 'File written'


