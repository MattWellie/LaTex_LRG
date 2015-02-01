import Bio


class GbkParser:
    """
    Class version: 0.1
    Modified Date: 01/02/2015
    Author : Matt Welland

    Notes:
        Isolated class to deal exclusively with GBK files
        Should return dictionary, not write full output

    Parses the input file to find all the useful values
    This will populate a dictionary to be returned at completion

            Dict { pad
                   genename
                   refseqname
                   transcripts {  transcript {   protein_seq
                                                 cds_offset
                                                 exons {  exon_number {   genomic_start
                                                                          genomic_stop
                                                                          transcript_start
                                                                          transcript_stop
                                                                          sequence (with pad)
    """

    def __init__(self, file_name, padding):

        """
        This class is created by instantiating with a file name and a padding value.
        These are used to locate the appropriate target file, and to select the
        amount of flanking sequence to be appended to exons.
        """
        '''
        :param file_name: the location/identity of the target input file
        :param padding: the required amount of intronic padding
        '''

        self.fileName = file_name
        # Read in the specified input file into a variable
        try:
            self.transcriptdict = dict(transcripts={}, input=Bio.SeqIO.to_dict(Bio.SeqIO.parse(file_name, 'genbank')),
                                       pad=int(padding),filename=self.fileName.split('.')[0] + '_' + padding,
                                       pad_offset= int(padding) % 5)
            self.transcriptdict['refseqname']=self.transcriptdict['input'].keys()[0]
            self.transcriptdict['transcripts'][1] = {}
            self.transcriptdict['transcripts'][1]['exons'] = {}
            self.is_matt_awesome = True
        except IOError as fileNotPresent:
            print "The specified file cannot be located: " + fileNotPresent.filename
            exit()

        assert self.transcriptdict['pad'] <= 2000, "Padding too large, please use a value below 2000 bases"

    def find_cds_delay_gbk(self, transcript):
        """ Method to find the actual start of the translated sequence
            introduced to sort out non-coding exon problems """
        '''
        :param transcript: currently a relic of the LRG process (29-01-2015), designed to separate the
                           dictionary population process into distinct sections for each transcript
        '''
        offset_total = 0
        offset = self.transcriptdict['transcripts'][transcript]['cds_offset']
        for exon in self.transcriptdict['transcripts'][transcript]['list_of_exons']:
            g_start = self.transcriptdict['transcripts'][transcript]['exons'][exon]['genomic_start']
            g_stop = self.transcriptdict['transcripts'][transcript]['exons'][exon]['genomic_end']
            if offset > g_stop:
                offset_total = offset_total + (g_stop - g_start)
            elif offset < g_stop and offset > g_start:
                self.transcriptdict['transcripts'][transcript]['cds_offset'] = offset_total + (offset - g_start)
                break

    def get_protein(self, cds):
        """
        This method takes the CDS tagged block from the GenBank features section and parses the
        contents to retrieve the protein sequence. This is added to the appropriate section of
        dictionary used to hold all required details of the file.
        """
        '''
        :param cds: a list containing the cds element(s) of the genbank features
        '''
        if len(cds) > 1: print "This gene has multiple transcripts, sort it out!"
        for x in cds:
            protein_sequence = x.qualifiers['translation'][0] + '* '
            self.transcriptdict['transcripts'][1]['protein_seq'] = protein_sequence

    def get_exons(self, exons):
        """
        This function is supplied with the list of exon tagged blocks from the features section
        and populates the exons region of the dictionary with the exon number, coordinates, and
        sequence segments whihc define the exon
        """
        '''
        :param exons: a list of the exon objects from the GenBank features list
        '''
        self.transcriptdict['transcripts'][1]['list_of_exons'] = []
        exon_count = 1
        for x in exons:
            # Some Genbank files do not feature explicitly numbered exons
            if 'number' in x.qualifiers:
                exon_number = x.qualifiers['number'][0]
            else:
                exon_number = str(exon_count)
                exon_count = exon_count + 1
            self.transcriptdict['transcripts'][1]['exons'][exon_number] = {}
            self.transcriptdict['transcripts'][1]['list_of_exons'].append(exon_number)
            location_feature = x.location
            self.transcriptdict['transcripts'][1]['exons'][exon_number]['genomic_start'] = location_feature.start
            self.transcriptdict['transcripts'][1]['exons'][exon_number]['genomic_end'] = location_feature.end
            sequence = self.transcriptdict['full genomic sequence'][location_feature.start:location_feature.end]
            if self.transcriptdict['pad'] != 0:
                pad = self.transcriptdict['pad']
                pad5 = self.transcriptdict['full genomic sequence'][
                       location_feature.start - (pad + 1):location_feature.start - 1]
                pad3 = self.transcriptdict['full genomic sequence'][
                       location_feature.end:location_feature.end + (pad + 1)]
                sequence = pad5.lower() + sequence + pad3.lower()
            self.transcriptdict['transcripts'][1]['exons'][exon_number]['sequence'] = sequence

    def run(self):
        """
        This is the main method of the GBK Parser. This method is called after class instantiation
        and handles the operation of all the other functions to complete the dictionary which will
        hold all of the sequence and exon details of the gene file being parsed
        """
        '''
        :return transcriptdict: This function fills and returns the dictionary, contents
                explained in Class docstring above
        '''
        # initial sequence grabbing and populating dictionaries
        dictionary = self.transcriptdict['input'][self.transcriptdict['refseqname']]
        self.transcriptdict['full genomic sequence'] = dictionary.seq
        features = dictionary.features
        exons = []
        cds = []
        # Sort through SeqFeatures to find the good stuff
        for feature in features:
            # Multiple exons are expected
            if feature.type == 'exon':
                exons.append(feature)
            # A single CDS is ideal, may cause some confusion if multiple exist
            # List handling is used to tidy up multiple CDS handling later
            elif feature.type == 'CDS':
                cds.append(feature)
        self.transcriptdict['genename'] = exons[0].qualifiers['gene'][0]
        self.get_protein(cds)
        self.get_exons(exons)
        self.transcriptdict['transcripts'][1]['cds_offset'] = cds[0].location.start
        self.find_cds_delay_gbk(1)
        return self.transcriptdict
