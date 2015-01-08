#Retry of existing reference sequence producer. 
#Various faults with formatting and exon handling exist in previous version
#Formatting and logic is also messy; this is a cleanup attempt

import sys
import xml.etree.ElementTree as etree
import os

class Parser:

    def __init__(self, file_name, padding, existingfiles):#, root, option):
        self.fileName = file_name
        #Read in the specified input file into a variable
        try:
            self.tree = etree.parse(self.fileName)
            self.root = self.tree.getroot()
            self.fixannot = self.root.find('fixed_annotation') #ensures only exons from the fixed annotation will be taken
            self.genename = self.root.find('updatable_annotation/annotation_set/lrg_locus').text    
            self.refseqname = self.root.find('fixed_annotation/sequence_source').text
            self.transcriptdict = {}
            self.existingfiles = existingfiles
        except IOError as fileNotPresent:
            print "The specified file cannot be located: " + fileNotPresent.filename
            exit()

        assert self.pad <= 2000, "Padding too large, please use a value below 2000 bases" 

    #Check the version of the file we are opening is correct
        if self.root.attrib['schema_version'] <> '1.9':
            print 'This LRG file is not the correct version for this script'
            print 'This is designed for v.1.8'
            print 'This file is v.' + self.root.attrib['schema_version']

#Grabs the sequence string from the <sequence/> tagged block
    def grab_element(self, path, root):
        '''Grabs specific element from the xml file from a provided path'''
        try:
            for item in self.root.findall(path):
                result = item.text
            return result
        except:
            print "No sequence was identified"


#Grab exon coords and sequences from the xml file 
    def get_exoncoords(self, level, pad, genseq):
            ''' Traverses the LRG eTree to find all the useful coordinate values and sequence elements      
                Since previous version this has become a dictionary with the following format
                (As opposed to lists of lists)
                Dict { transcript {   protein_seq 
                                      cds_offset
                                      exons {  exon_number {   genomic_start
                                                               genomic_stop
                                                               transcript_start
                                                               transcript_stop
                                                               sequence (with pad)

                This should allow more robust use of the stored values, and enhances transparency of the
                methods put in place. Absolute references should also make the program more easily extensible
            '''
        for items in level.findall('transcript'):
            t_number = int(items.attrib['name'][1:])    #e.g. 't1', 't2'
            self.transcriptdict[t_number] = {} #first should be indicated with '1'; 'p1' can write on
            self.transcriptdict[t_number]["exons"] = {}
            #Gene sequence main coordinates are required to take introns
            #Transcript coordinates wanted for output
            genomic_start = 0
            genomic_end = 0
            transcript_start = 0
            transcript_end = 0
            for exon in items.iter('exon'):
                exon_number = int(exon.attrib['label'])
                self.transcriptdict[t_number]["exons"][exon_number] = {}
                for coordinates in exon:
                    #Find Transcript Coordinates
                    if coordinates.attrib['coord_system'][-2] == 't':
                        self.transcriptdict[t_number]["exons"][exon_number]['transcript_start'] = int(coordinates.attrib['start'])
                        self.transcriptdict[t_number]["exons"][exon_number]['transcript_end'] = int(coordinates.attrib['end'])                   
                    if coordinates.attrib['coord_system'][-2] not in ['t', 'p']:
                        genomic_start = int(coordinates.attrib['start'])
                        genomic_end = = int(coordinates.attrib['end'])
                assert genomic_start >= 0, "Exon index out of bounds"
                assert genomic_end <= len(genseq), "Exon index out of bounds"
                seq = genseq[genomic_start-1:genomic_end]
                if pad > 0:					
                    assert genomic_start - pad >= 0, "Exon index out of bounds"
                    assert genomic_end + pad <= len(genseq), "Exon index out of bounds"
                    pad5 = genseq[genomic_start-pad:genomic_start]
                    pad3 = genseq[genomic_end:genomic_end+pad]
                    seq = pad5.lower() + seq + pad3.lower()
                    self.transcriptdict[t_number]["exons"][exon_number]['sequence'] = seq
                    self.transcriptdict[t_number]["exons"][exon_number]['genomic_start'] = genomic_start
                    self.transcriptdict[t_number]["exons"][exon_number]['genomic_end'] = genomic_end
        return transcriptdict
    
    def get_protein_exons(self, prot_level):
        ''' collects full protein sequence for the appropriate transcript '''
        for item in level.findall('transcript'):
            p_number = int(item.attrib['name'][1:])            
            coding_region = item.find('coding_region')
            coordinates = coding_region.find('coordinates')
            self.transcriptdict[p_number]['cds_offset'] = int(coordinates.attrib['start'])
            
            translation = coding_region.find('translation')
            sequence = translation.find('sequence').text
            self.transcriptdict[p_number]['protein_seq'] = sequence+'*' # Stop codon

    def find_cds_delay(self):
        ''' Method to find the actual start of the translated sequence
            introduced to sort out non-coding exon problems '''
        #STUB

    def print_latex(self, transcript, outfile):
        latex_dict = self.transcriptdict[transcript]
        ''' Creates a LaTex readable file which can be converted to a final document
	        Currently only working for DNA sequences
            Lengths of numbers calculated using len(###)'''
        protein = latex_dict['protein_seq']
        refseqid = rself.refseqname.replace('_', '\_')#Required for LaTex
        CDS_count = 1 - latex_dict[cds_offset] #A variable to keep a count of the 
                                               #transcript length across all exons

	    #The initial line(s) of the LaTex file, required to run
        self.line_printer('\\documentclass{article}', outfile)
        self.line_printer('\\usepackage{fancyvrb}', outfile)
        self.line_printer('\\begin{document}', outfile)
        self.line_printer('\\begin{center}', outfile)        
        self.line_printer('\\begin{large}', outfile)
        self.line_printer(' Gene: %s - Sequence: %s' % (self.genename, refseqid), outfile)
        self.line_printer(' Date : \\today', outfile)
        self.line_printer('\\end{large}', outfile)
        self.line_printer('\\end{center}', outfile)
        self.line_printer(' \\begin{Verbatim}', outfile)

        wait_value = 0
        codon_count = 3         #Print on first codon
        amino_acid_counter = 0
        amino_wait = 0
        amino_number = ''
        amino_number_string = []
        amino_printing = False
        number_to_print = ''
        codon_numbered = False
        number_string  = [] 
        dna_string = []
        amino_string = []
        amino_number_string = []
        for exon in latex_dict['list_of_exons']:
            exon_dict = latex_dict['exons'][exon]
            tran_start = exon_dict['trancript_start']
            tran_end = exon_dict['trancript_end']
            sequence = exon_dict['sequence']
            self.line_printer(' ', outfile)
            self.line_printer('Exon %s | Start: %s | End: %s | Length: %d' % (str(exon), str(tran_start), str(tran_end), (tran-end - tran_start), outfile)
            line_count = 0

            for char in sequence:
                #Stop each line at a specific length
                #Remainder method prevents count being 
                #print amino_acid_counter
                if line_count%60 == 0:
                    if wait_value != 0:
                        for x in range(wait_value + 1)[::-1]:
                            number_to_print = number_to_print[::-1]
                            number_string.append(number_to_print[x])
                        wait_value = 0
                    if amino_wait != 0:
                        for x in range(amino_wait)[::-1]:
                            amino_number = amino_number[::-1]
                            amino_number_string.append(amino_number[x-1])
                        amino_wait = 0
                    self.line_printer(number_string, outfile)
                    self.line_printer(dna_string, outfile)
                    self.line_printer(amino_string, outfile)
                    self.line_printer(amino_number_string, outfile)
                    self.line_printer('   ', outfile)
                    amino_string = []
                    number_string = []
                    dna_string = []
                    amino_number_string = []
                dna_string.append(char)
                if CDS_count == 1:
                    amino_printing = True
                if amino_acid_counter >= len(protein):
                    amino_printing = False
                if amino_printing == True and char.isupper():
                    if codon_count == 3:
                        amino_string.append(protein[amino_acid_counter])
                        amino_acid_counter = amino_acid_counter + 1
                        codon_numbered = False
                        codon_count = 1
                    else:
                        codon_count = codon_count + 1
                        amino_string.append(' ')
                else:
                    amino_string.append(' ') 
                
                if char.isupper() and amino_acid_counter < len(protein):
                    if (CDS_count % 10 == 1) or (CDS_count == 1) and (wait_value != 0) and (CDS_count >= 1) and (CDS_count <= CDS_length):
                        number_string.append('|')
                        number_to_print = str(CDS_count)[::-1]
                        wait_value = len(number_to_print)-1
                        CDS_count = CDS_count + 1
                    elif wait_value != 0:
                        number_string.append(number_to_print[wait_value-1])
                        CDS_count = CDS_count + 1 
                        wait_value = wait_value - 1
                    else:
                        number_string.append(' ')
                        CDS_count = CDS_count + 1   
                else:
                    if wait_value != 0:
                        number_string.append(number_to_print[wait_value-1])
                        wait_value = wait_value - 1
                    else:
                        number_string.append(' ')
                
                #Amino Acid numbering
                if amino_acid_counter %10 == 1 and codon_numbered == False:
                    amino_number_string.append('|')
                    amino_number = str(amino_acid_counter)[::-1]
                    amino_wait = len(amino_number)-1
                    codon_numbered = True
                elif amino_wait != 0:
                    amino_number_string.append(amino_number[amino_wait-1])
                    amino_wait = amino_wait - 1
                elif amino_acid_counter %10 != 1 and amino_wait == 0:
                    amino_number_string.append(' ')
                line_count += 1
            
            #Section for incomplete lines (has not reached line-limit print)
            if len(dna_string) != 0:
                if wait_value != 0:
                    for x in range(wait_value):
                        number_string.append(number_to_print[x-1])
                    wait_value = 0
                if amino_wait != 0:
                    for x in range(amino_wait):
                        amino_number_string.append(amino_number[x-1])
                    amino_wait = 0
                self.line_printer(number_string, outfile)
                self.line_printer(dna_string, outfile)
                self.line_printer(amino_string, outfile)
                self.line_printer(amino_number_string, outfile)
                self.line_printer('  ', outfile)

        self.line_printer('\\end{Verbatim}', outfile)       
        self.line_printer('\\end{document}', outfile)

    def line_printer(self, string, outfile):
        print >>outfile, ''.join(string)

    def run(self):
        
        #initial sequence grabbing and populating dictionaries
        gen_seq = self.grab_element('fixed_annotation/sequence', self.root)
        self.get_exoncoords(self.fixannot, self.pad, gen_seq)
        self.get_protein_exons(self.fixannot)
        for transcript in self.transcriptdict.keys():
            number_of_exons = len(self.transcriptdict[transcript]['exons'])
            self.transcriptdict[transcript]['number_of_exons'] = number_of_exons
            exon_list = range(number_of_exons)
            for x in exon_list:
                x = x + 1
            self.transcriptdict[transcript]['list_of_exons'] = exon_list

        #finding cds offset
        self.find_cds_delay()

        for entry in self.transcriptdict.keys():
            outputfile = self.fileName.split('.')[0]+'_'+entry+"_"+str(self.pad)
            outputfilename = outputfile + '.tex'
            outputFilePath = 'outputFiles/' + outputfilename
            if outputfile in self.existingFiles:
            #tests whether file already exists
                print 'The output file already exists in the present directory'
                print 'Would you like to overwrite the file? y/n'
                c = 0
                while c == 0:
                    userChoice = raw_input('> ')
                    if userChoice == 'n':
                        print "Program exited without creating file"
                        exit() # can change later to offer alternate filename
                    elif userChoice == 'y':
                        c += 1
                    else:
                        print "Invalid selection please type y or n"
            out = open(outputFilePath, "w")
            self.print_latex(entry, out)
            return outputfile