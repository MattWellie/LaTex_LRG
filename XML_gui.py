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
    entry.insert(0, name)
def About():
    print "This is a simple example of a menu"
    #Operating instructions

#OS methods (not fixed for class)
#A fair amount of hard-coding is in place, just to ensure that output is in folders

def run_parser():
    #Files will not be stored directly in outputFiles anymore - requires overwrite check
    existingFiles = os.listdir('outputFiles')
    option = v.get()
    directory_and_file= entry.get()
    file_name = directory_and_file.split('/')[-1]
    padding = pad.get()
    xml_parser = Parser(file_name, padding, option, existingFiles)
    print 'Running parser'
    latex_file = xml_parser.run()
    os.chdir("outputFiles")
    os.mkdir(latex_file[0:-4]) # Try-catch, this folder may exist
    shutil.move(latex_file, os.path.join(latex_file[0:-4], latex_file))
    os.chdir(latex_file[0:-4])
    call(["pdflatex", latex_file])
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
button = Button(root, text="Browse...", command=open_file)
button.grid(row=0, column=3)

padding_in_label = Label(root, text="Intronic padding:")
padding_in_label.grid(row=1, column=1, sticky = 'w')
pad = Entry(root)
pad.grid(row=1,column=2, sticky = 'w')
pad.insert(0, "0")

v=StringVar()
v.set('-g')
gen_radio = Radiobutton(root, text="Genomic only", variable=v, value='-g')#, command=set_option(value))
prot_radio = Radiobutton(root, text="Protein only", variable=v, value='-p')#, command=set_option(value))
both_radio = Radiobutton(root, text="Genomic + Protein", variable=v, value='-pg')#, command=set_option(value))
gen_radio.grid(row=2, column=1, sticky = 'w')
prot_radio.grid(row=2, column=2)
both_radio.grid(row=2, column=3)

button = Button(root, text="QUIT", fg="red", command=root.quit)
button.grid(row=3, column=1)
parser= Button(root, text="Translate", fg="blue", command=run_parser)
parser.grid(row=3, column=2)

mainloop()
