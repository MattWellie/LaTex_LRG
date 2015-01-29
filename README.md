##License 
At some point I'll work out what kind of license this should have...
It's open source anyway...

##Requirements and testing

pdflatex/texlive/miktex

tkinter (python graphics package)

BioPython (GenBank file parsing, not required for LRG file references)

Python 2.7

##What it does

- This program takes a file as input and creates a typeset reference sequence.
This sequence is designed to be used during sequence checking, and includes an
HGVS nomenclature naming system.

- This ensures platform independence through use of platform-ambivalent file paths
and naming conventions. 

- Internal logic allows files in valid GenBank or LRG formats to be used as input
without making any changes to the program code.

##Who its for

##How to operate it
- At command line: *python XML_gui.py* without any additional arguments

- This command will bring up the main interface, offering two entry boxes. 

- The top entry box can either be edited directly or by using the 'Browse...' button. This will show the local directory
and allow file selection directly.

- There is a 'Help' button on the ribbon which will print a brief guide statement
to the command line. This can be edited in the XML_gui.py file

##Planned updates

- The program currently ignores input files with multiple transcripts, this should be handled appropriately

- The program has been broken up into several different components;
    - XML_gui.py to show the user interface
    - LRG/GBK_Parser.py to read the input file into a dictionary
    - reader.py to read the dictionary into an output format
    - latex_writer.py to write the reader output into an output file and call a pdflatex command to typeset the file


##Issue Tracker
- stumbles on exons numbered with letters (e.g. 14a) due to a failed sorting mechanism, otherwise works
        - A workaround is in place for this, which checks to see if a genbank exon has a number, if not a serial number is created. As things stand this will wrongly label genes with skipped exon numbers, or multiple exons of the same number (14a, 14b... though this is most likely to occur on parallel transcripts). A similar or better workaround could be put into the LRG variant

- Requires a statement to check if the first base of the first exon is 1 (no 5' UTR) in which case a warning should be printed, and a preceeding intronic sequence should not be grabbed (will read from the end of the sequence due to negative reference (BRCA1 as an example)


###Tinkering:

To have the amino acid appear below different bases within the codon:
* set the variable codon_count in print_latex() to:
    - 3 to print with the first base of the codon
    - 2 to print in the middle
    - 1 to print below the final base

The protein sequence is grabbed as a single uninterrupted sequence, so none of these 
approaches will affect the number of AAs printed, only the positions. However, this 
may change which exon the AA is printed in (if a codon is across exons)


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
