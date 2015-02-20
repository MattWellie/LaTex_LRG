##License 
At some point I'll work out what kind of license this should have...
It's open source anyway...

##Requirements and testing

pdflatex/texlive/miktex (For LaTex production, not required for text document (see write\_as\_latex in Xml_GUI)

tkinter (python graphics package)

BioPython 1.65 (GenBank file parsing, not required for LRG file references)

Python 2.7

##What it does

- This program takes a file as input and creates a typeset reference sequence.
This sequence is designed to be used during sequence checking, and includes an
HGVS nomenclature naming system.

- This ensures platform independence through use of platform-ambivalent file paths
and naming conventions. 

- Separation into discrete paths allows files in valid GenBank or LRG formats to be used as input
without making any changes to the program code.

##Who its for

This is intended for use by any genetic scientist who may require a hard-copy of a genetic sequence 
for checking against when signing off reports. This is intended to replace the existing procedure
of manually creating reference sequence copies by using a uniform typesetting style and format for
all inputs.

##How to operate it
- At command line: *python XML_GUI.py* without any additional arguments. This can be done using *python X -> Tab*

- This command will bring up the main interface, offering two entry boxes. 

- The top entry box can either be edited directly or by using the 'Browse...' button. This 
will show the local directory and allow file selection directly. This is where to insert the
filename you wish to convert.

- There is a 'Help' button on the ribbon which will print a brief guide statement
to the command line. This can be edited in the XML_gui.py file

##How it works

- The program has been broken up into several different components;
    - XML_gui.py to show the user interface
    - LRG/GBK_Parser.py to read the input file into a dictionary
    - reader.py to read the dictionary into a list output format
    - writer.py to read the list into an actual file
    - latex_writer.py to write the reader output into a external file 
    - The XML_GUI.py module then calls a pdflatex command to typeset the file

##Planned updates

- As of 10/02/2015 there are no significant updates, only minor improvements
- Please feel free to suggest any improvements you require

##Issue Tracker
- stumbles on exons numbered with letters (e.g. 14a) due to a failed sorting mechanism, otherwise works
        - A workaround is in place for this, which checks to see if a genbank exon has a number, if not a serial number is created. As things stand this will wrongly label genes with skipped exon numbers, or multiple exons of the same number (14a, 14b... though this is most likely to occur on parallel transcripts). A similar or better workaround could be put into the LRG variant

- Requires a statement to check if the first base of the first exon is 1 (no 5' UTR) in which case a warning should be printed, and a preceeding intronic sequence should not be grabbed (will read from the end of the sequence due to negative reference (BRCA1 as an example)

- A real corner case... If the output type is set to .txt and the input file contains multiple transcripts, the
output files may be created so quickly that a second will not pass between the first and second file being created.
This can cause the program to try and create an existing folder, which will throw an error. (seen on LRG.214.xml)



###Tinkering:

To have the amino acid appear below different bases within the codon:
* set the variable codon_count in print_latex() to:
    - 3 to print with the first base of the codon
    - 2 to print in the middle
    - 1 to print below the final base

The protein sequence is grabbed as a single uninterrupted sequence, so none of these 
approaches will affect the number of AAs printed, only the positions. However, this 
may change which exon the AA is printed in (if a codon is across exons)

To have the program print a .txt format file instead of using LaTex (useful in a pinch if the workstation
does not have an installation of LaTex available):
* set the write_as_latex variable in XML_GUI.py to False

There are two variables in the XML_GUI class which can be used to determine how the application 
handles exon boundaries where the flanking intron containss a region of the next intron. 
* trim_flanking
    - If True, the intronic sequence will be made shorter to avoid any appearance of the next (or previous) exon as intronic sequence
    - If False, the program will not interfere and a full flanking region will be printed regardless of overlap

* print_clashes
    - If True, a line will be printed underneath the exon header of each exon involved in an overlap (regardless of having been trimmed to avoid overlap) to state that there is an overlap, and to say whether it is over the previous, next, or both
    - If False, no warning messages are printed, whether or not a trim has been used


─────────▄──────────────▄<br>
────────▌▒█───────────▄▀▒▌<br>
────────▌▒▒▀▄───────▄▀▒▒▒▐<br>
───────▐▄▀▒▒▀▀▀▀▄▄▄▀▒▒▒▒▒▐<br>
─────▄▄▀▒▒▒▒▒▒▒▒▒▒▒█▒▒▄█▒▐<br>
───▄▀▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▀██▀▒▌<br>
──▐▒▒▒▄▄▄▒▒▒▒▒▒▒▒▒▒▒▒▒▀▄▒▒▌<br>
──▌▒▒▐▄█▀▒▒▒▒▄▀█▄▒▒▒▒▒▒▒█▒▐<br>
─▐▒▒▒▒▒▒▒▒▒▒▒▌██▀▒▒▒▒▒▒▒▒▀▄▌<br>
─▌▒▀▄██▄▒▒▒▒▒▒▒▒▒▒▒░░░░▒▒▒▒▌<br>
─▌▀▐▄█▄█▌▄▒▀▒▒▒▒▒▒░░░░░░▒▒▒▐<br>
▐▒▀▐▀▐▀▒▒▄▄▒▄▒▒▒▒▒░░░░░░▒▒▒▒▌<br>
▐▒▒▒▀▀▄▄▒▒▒▄▒▒▒▒▒▒░░░░░░▒▒▒▐<br>
─▌▒▒▒▒▒▒▀▀▀▒▒▒▒▒▒▒▒░░░░▒▒▒▒▌<br>
─▐▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▐<br>
──▀▄▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▄▒▒▒▒▌<br>
────▀▄▒▒▒▒▒▒▒▒▒▒▄▄▄▀▒▒▒▒▄▀<br>
───▐▀▒▀▄▄▄▄▄▄▀▀▀▒▒▒▒▒▄▄▀<br>
 ──▐▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▀▀<br>

#Happy hunting
