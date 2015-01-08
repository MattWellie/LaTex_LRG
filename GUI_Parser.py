#Program to import a specified LRG file and export corresponding fasta
import sys
import xml.etree.ElementTree as etree
import os
#Read input arguments - should be
# [0] - program name
# [1] - Input XML file name
# [2] - Padding length (intronic surrounding exons)
# [3] - "-g" for genomic sequence, "-p" for protein
#Read input file name from arguments

class Parser:

    def __init__(self, file_name, padding, existingFiles):#, root, option):
        self.fileName = file_name
        self.existingFiles = existingFiles
        #assert len(sys.argv) <=4, "Too many arguments!" #check no additional arguments provided on command line
        #Check file name is valid .xml
        assert self.fileName[-4:] == '.xml', 'You have the wrong input file' 
        #Scan for the optional argument specifying genomic/protein etc.

        #Read in the specified input file into a variable
        try:
            self.tree = etree.parse(self.fileName)
            self.root = self.tree.getroot()
            self.fixannot = self.root.find('fixed_annotation') #ensures only exons from the fixed annotation will be taken
            self.genename = self.root.find('updatable_annotation/annotation_set/lrg_locus').text    
            self.CDS_offset_path = 'fixed_annotation/transcript/coding_region/coordinates'
            self.prot_path = 'fixed_annotation/transcript/coding_region/translation'
            self.refseqname = self.root.find('fixed_annotation/sequence_source').text
        except IOError as fileNotPresent:
            print "The specified file cannot be located: " + fileNotPresent.filename
            exit()
        self.CDS_offset = 0
        self.CDS_length = 0
        try:
            self.pad = int(padding)
        except:
            self.pad = 0
            print "Invalid/No padding provided: Padding defaulting to zero"
        #LRG files have 2000 additional genomic sequence on 3' side, set as max
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
        '''Traverses the XML eTree to identify all the exons for the sequence
        Returns a dictionary containing exon numbers, start and finish
        co-ordinates, and the appropriate chunk of sequence.
        The dictionary is designed to be passed to a dedicated write function
        which will print the appropriate sequence elements and identifiers to
        an output file'''
        transcriptdict = {}	#LRG files can contain more than one transcript in fixed annotation section
        for items in level.findall('transcript'):
            self.DNA_transcript = items.attrib['name']
            tranexons = []
            #Gene sequence main coordinates are required to take introns
            #Transcript coordinates wanted for output
            genStart = 0
            genEnd = 0
            CDS_holder = self.root.findall(self.CDS_offset_path)
            for item in CDS_holder:
                self.CDS_offset = int(item.attrib['start'])
                self.CDS_length = int(item.attrib['end']) - int(item.attrib['start'])
            for exon in items.iter('exon'):
                if exon.attrib['label'] == '1':
                    for coordinates in exon:
                        if coordinates.attrib['coord_system'][-2] not in ['t', 'p']:
                            startIndex = int(coordinates.attrib['start'])
                            self.CDS_offset = self.CDS_offset - startIndex
                for coordinates in exon:
                    if coordinates.attrib['coord_system'][-2] == 't':
                        genStart = int(coordinates.attrib['start'])
                        genEnd = int(coordinates.attrib['end'])
                    if coordinates.attrib['coord_system'][-2] not in ['t', 'p']:
                        #ensures only genomic coords are taken
                        startIndex = int(coordinates.attrib['start'])
                        endIndex = int(coordinates.attrib['end'])
                        assert startIndex >= 0, "Exon index out of bounds"
                        #print "Start Index: " + str(startIndex)
                        assert endIndex <= len(genseq), "Exon index out of bounds"
                        seq = genseq[startIndex-1:endIndex]
                        if pad > 0:					
                            assert startIndex - pad >= 0, "Exon index out of bounds"
                            assert endIndex + pad <= len(genseq), "Exon index out of bounds"
                            pad5 = genseq[startIndex-pad:startIndex]
                            pad3 = genseq[endIndex:endIndex+pad]
                            seq = pad5.lower() + seq + pad3.lower()
                tranexons.append((exon.attrib['label'], genStart, genEnd, seq, startIndex, endIndex))
                    #can add extra elif options to grab other sequence types
            transcriptdict[self.DNA_transcript] = tranexons
        return transcriptdict
    
    
    def get_protein_exons(self, prot_level, root):
        ''' Cut down, only collects full protein sequence '''
        proteindict = {} #to contain exons from protein sequence
        for item in root.findall(prot_level):
            try:
                prot_block = item.find("sequence")
                protein_seq = prot_block.text
                self.prot_transcript = item.attrib['name']
            except:
                print "No protein sequence was found"   
            proteindict[self.prot_transcript] = protein_seq
        return proteindict

    def print_latex(self, exoncoordlist, protein, transcript, gene, refseqid, outfile):

        ''' Creates a LaTex readable file which can be converted to a final document
	        Currently only working for DNA sequences
            Lengths of numbers calculated using len(###)'''

        refseqid = refseqid.replace('_', '\_')#Required for LaTex
        CDS_count = 1 - self.CDS_offset       #A variable to keep a count of the 
                                              #transcript length across all exons
	    #The initial line(s) of the LaTex file, required to run
        self.line_printer('\\documentclass{article}', outfile)
        self.line_printer('\\usepackage{fancyvrb}', outfile)
        self.line_printer('\\begin{document}', outfile)
        self.line_printer('\\begin{center}', outfile)        
        self.line_printer('\\begin{large}', outfile)
        self.line_printer(' Gene: %s - Sequence: %s' % (gene, refseqid), outfile)
        self.line_printer(' Date : \\today', outfile)
        self.line_printer('\\end{large}', outfile)
        self.line_printer('\\end{center}', outfile)
        self.line_printer(' \\begin{Verbatim}', outfile)
        wait_value = 0
        codon_count = 3
        amino_acid_counter = 0
        amino_wait = 0
        amino_number = ''
        amino_number_string = []
        amino_printing = False
        number_to_print = ''
        codon_numbered = False
        for exon in range(len(exoncoordlist)):
            DNA_exon = exoncoordlist[exon]
            print >>outfile, '\n\n\n Exon %s | Start: %s | End: %s | Length: %d \n' % (str(DNA_exon[0]), str(DNA_exon[1]), str(DNA_exon[2]), (DNA_exon[2]-DNA_exon[1]))
            line_count = 0
            number_string  = [] 
            dna_string = []
            amino_string = []
            amino_number_string = []

            for char in DNA_exon[-3]:
                #Stop each line at a specific length
                #Remainder method prevents count being 
                #print amino_acid_counter
                if line_count%60 == 0:
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
                   
                if char.isupper():
                    if (CDS_count % 10 == 1) or (CDS_count == 1) and (wait_value != 0) and (CDS_count >= 1) and (CDS_count <= CDS_length):
                        number_string.append('|')
                        number_to_print = str(CDS_count)[::-1]
                        wait_value = len(number_to_print)
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
                    amino_wait = len(amino_number)
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
        
        gen_seq = self.grab_element('fixed_annotation/sequence', self.root)
        td = self.get_exoncoords(self.fixannot, self.pad, gen_seq)
        pd = self.get_protein_exons(self.prot_path, self.root)
        for entry in range(len(td)):
            exons = td[td.keys()[entry]]
            protein = pd[pd.keys()[entry]]
        #for y in td.keys():
            outputfile = self.fileName.split('.')[0]+'_'+td.keys()[entry]+"_"+str(self.pad)+'_Out.tex'
            outputFilePath = 'outputFiles/' + outputfile
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
            self.print_latex(exons, protein, td.keys()[entry], self.genename, self.refseqname, out)
            return outputfile