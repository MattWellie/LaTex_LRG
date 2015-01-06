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

    def __init__(self, file_name, padding, option, existingFiles):#, root, option):
        self.fileName = file_name
        self.existingFiles = existingFiles
        #assert len(sys.argv) <=4, "Too many arguments!" #check no additional arguments provided on command line
        #Check file name is valid .xml
        assert self.fileName[-4:] == '.xml', 'You have the wrong input file' 
        #Scan for the optional argument specifying genomic/protein etc.
        #If option is not identified, use genomic only
        self.option = ''
        try:
            self.option = option
        except:
            self.option = '-g'
        #print 'option: ', option
        #Read in the specified input file into a variable
        try:
            self.tree = etree.parse(self.fileName)
            self.root = self.tree.getroot()
            self.fixannot = self.root.find('fixed_annotation') #ensures only exons from the fixed annotation will be taken
            self.genename = self.root.find('updatable_annotation/annotation_set/lrg_locus').text    
            self.prot_path = 'fixed_annotation/transcript/coding_region/translation'
            self.refseqname = self.root.find('fixed_annotation/sequence_source').text
        except IOError as fileNotPresent:
            print "The specified file cannot be located: " + fileNotPresent.filename
            exit()

        try:
            self.pad = int(padding)
        except:
            self.pad = 0
            print "Invalid/No padding provided: Padding defaulting to zero"
        #LRG files have 2000 additional genomic sequence on 3' side, set as max
        assert self.pad <= 2000, "Padding too large, please use a value below 2000 bases" 

    #Check the version of the file we are opening is correct
        if self.root.attrib['schema_version'] <> '1.8':
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
            for exon in items.iter('exon'):
                for coordinates in exon:
                    if coordinates.attrib['coord_system'][-2] not in ['t','p']:
                        #ensures only genomic coords are taken
                        startIndex = int(coordinates.attrib['start'])
                        endIndex = int(coordinates.attrib['end'])
                        assert startIndex >= 0, "Exon index out of bounds"
                        assert endIndex <= len(genseq), "Exon index out of bounds"
                        seq = genseq[startIndex-1:endIndex]
                        if pad > 0:					
                            assert startIndex - pad >= 0, "Exon index out of bounds"
                            assert endIndex + pad <= len(genseq), "Exon index out of bounds"
                            pad5 = genseq[startIndex-pad:startIndex]
                            pad3 = genseq[endIndex:endIndex+pad]
                            seq = pad5.lower() + seq + pad3.lower()
                        tranexons.append((exon.attrib['label'],startIndex, endIndex,seq))
                    #can add extra elif options to grab other sequence types
            transcriptdict[self.DNA_transcript] = tranexons
        return transcriptdict
    
    
    def get_protein_exons(self, prot_level, exon_level, root):
        proteindict = {} #to contain exons from protein sequence
        for item in root.findall(prot_level):
            try:
                prot_block = item.find("sequence")
                protein_seq = prot_block.text
                #print protein_seq    
                self.prot_transcript = item.attrib['name']
                #print transcript
            except:
                print "No protein sequence was found"   
            protexons = []
            #print 'for exon in...'
            for exon_item in root.findall(exon_level):
                exon_counter = 0
                for exon in exon_item.iter('exon'):
                    exon_counter = exon_counter + 1
                    #print 'for coord in exon'
                    attribute_list = []
                    for coordinates in exon: 
                        attribute_list.append(coordinates.attrib['coord_system'][-2:])
                    if self.prot_transcript in attribute_list:
                        for coordinates in exon: 
                            if coordinates.attrib['coord_system'][-2:] == self.prot_transcript:
                                start_index = int(coordinates.attrib['start'])
                                end_index = int(coordinates.attrib['end'])
                                assert start_index >= 0, "Exon index out of bounds"
                                assert end_index <= len(protein_seq), "Exon index out of bounds"
                                seq = protein_seq[start_index-1:end_index]
                                protexons.append((exon.attrib['label'], start_index, end_index,seq))
                    else:
                        protexons.append((exon_counter, 0, 0, ''))
            proteindict[self.prot_transcript] = protexons
            #print proteindict
        return proteindict


    def print_exons(self, exoncoordlist, transcript, gene, refseqid, outfile):
        '''Prints the exon sequences with headers to a fasta file'''
        for ex in exoncoordlist:
            header = ">Exon_" + str(ex[0]) + "|" + gene + "|" + refseqid +'|LengthOfExon:' + str(ex[2]-ex[1]) + "|StartPos:"+str(ex[1]) + "|EndPos:"+str(ex[2])
            print >>outfile, header,"\n",ex[-1]
    
    def print_latex(self, exoncoordlist, transcript, gene, refseqid, outfile):
        CDS_position = 0
        '''prints a LaTex file containing the results'''
        #print exoncoordlist
        self.line_printer('\\documentclass{article}\n\\usepackage{fancyvrb}\n\\begin{document}\n\\begin{Verbatim}', outfile)
        for exon in range(len(exoncoordlist)):
            #print exon
            DNA_exon = exoncoordlist[exon]
            print >>outfile, '\n\n Exon %s| Start: %s | End: %s \n\n' % (str(DNA_exon[0]), str(DNA_exon[1]), str(DNA_exon[2]))
            count = 0
            number_count = 0
            number_string  = [] 
            dna_string = []
            for char in DNA_exon[-1]:
                if count%50 == 0:
                    #count = 0
                    #number_string.append('\\newline')
                    self.line_printer(number_string, outfile)
                    #dna_string.append('\\newline')
                    self.line_printer(dna_string, outfile)
                    number_string = []
                    dna_string = []
                dna_string.append(char)
                if char.isupper():
                    if (number_count % 10 == 0) or (number_count == 0):
                        number_string.append('|')
                    else:
                        number_string.append(' ')    
                else:
                    number_string.append(' ')
                number_count += 1
                count += 1
                #print number_count

            if len(dna_string) != 0:
                number_string = []
                for char in dna_string:
                    if char.isupper():
                        if (number_count % 10 == 0) or (number_count == 0):
                            number_string.append('|')
                        else:
                            number_string.append(' ')
                    number_count += 1
                #number_string.append('\\newline')
                self.line_printer(number_string, outfile)
                self.line_printer(dna_string, outfile)
        self.line_printer('\\end{Verbatim}', outfile)       
        self.line_printer('\\end{document}', outfile)

    def line_printer(self, string, outfile):
        print >>outfile, ''.join(string)

    def print_both(self, prot_list, exon_list, gene, refseqid, outfile):
        '''Prints the file header, DNA seq, and protein seq for each exon.
        Not strictly FastA, but required for WMRGL'''
        for exon in range(len(prot_list)):
            DNA_exon = exon_list[exon]
            PROT_exon = prot_list[exon]
            header = ">Exon_" + DNA_exon[0] + "|" + gene + "|" + refseqid +'|LengthOfDNA:' + str((DNA_exon[2]-1)-DNA_exon[1])+'|LengthOfProt:' + str(( PROT_exon[2]+1)-PROT_exon[1]) + "|DNA_StartPos:"+str(DNA_exon[1]) + "|DNA_EndPos:"+str(DNA_exon[2])+"|PROT_StartPos:"+str(PROT_exon[1]) +   "|PROT_EndPos:"+str(PROT_exon[2])
            print >>outfile, header
            print >>outfile, DNA_exon[-1]
            print >>outfile, PROT_exon[-1]
        

    def run(self):
        #if elif options for which sequences need to be grabbed 
        if self.option == '-g':
            gen_seq = self.grab_element('fixed_annotation/sequence', self.root)
            td = self.get_exoncoords(self.fixannot, self.pad, gen_seq)
            for y in td.keys():
                outputfile = self.fileName.split('.')[0]+'_'+y+"_"+str(self.pad)+'_Out.tex'
                outputFilePath = 'outputFiles\\' + outputfile
                #print outputFilePath
                #print self.existingFiles
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
                self.print_latex(td[y], y, self.genename, self.refseqname, out)
                return outputFilePath
        
        elif self.option == '-p':
            dnaSeq = self.grab_element('fixed_annotation/sequence', self.root)
            pd = self.get_protein_exons(self.prot_path, 'fixed_annotation/transcript', self.root)
            for y in pd.keys():
                outputfile = self.fileName.split('.')[0]+'_'+y+"_"+'_Prot_Out.fasta'
                outputFilePath = 'outputFiles\\' + outputfile
                print 'output path: ', outputFilePath
                #self.existingFiles = os.listdir('outputFiles')
                #print 'Existing files: ', existingFiles
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
                self.print_exons(pd[y], y, self.genename, self.refseqname, out)
                return outputFilePath
        else:
            dnaSeq = self.grab_element('fixed_annotation/sequence', self.root)
            td = self.get_exoncoords(self.fixannot, self.pad, dnaSeq)
            pd = self.get_protein_exons(self.prot_path, 'fixed_annotation/transcript', self.root)
            assert len(pd) == len(td), "The number of transcripts are different, please check file"
            for entry in range(len(td)):
                y = td[td.keys()[entry]]
                p = pd[pd.keys()[entry]]
                assert len(y) == len(p), "The number of exons are different, please check file"
                outputfile = str(self.fileName.split('.')[0])+'_DNA'+self.DNA_transcript+"-Prot"+self.prot_transcript+"_"+str(self.pad)+'intronic_DNA_PROT_Out.fasta'
                #print outputfile
                outputFilePath = 'outputFiles\\' + outputfile
                #existingFiles = os.listdir('outputFiles')
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
                self.print_both(p, y, self.genename, self.refseqname, out)
                return outputFilePath