import Bio
from Bio import SeqIO

__author__ = 'mwelland'
__version__ = 0.3
__version_date__ = '11/02/2015'

class GbkParser:
    """
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
        self.exons = []
        self.cds = []
        self.mrna = []
        self.fileName = file_name
        # Read in the specified input file into a variable
        try:
            self.transcriptdict = dict(transcripts={}, input=SeqIO.to_dict(SeqIO.parse(file_name, 'genbank')),
                                       pad=int(padding), filename=self.fileName.split('/')[-1].split('.')[0] + '_' + str(padding),
                                       pad_offset=int(padding) % 5)
            self.transcriptdict['refseqname'] = self.transcriptdict['input'].keys()[0]
            self.is_matt_awesome = True
        except IOError as fileNotPresent:
            print "The specified file cannot be located: " + fileNotPresent.filename
            exit()

        assert self.transcriptdict['pad'] <= 2000, "Padding too large, please use a value below 2000 bases"

    @property
    def get_version(self):
        """
        Quick function to grab version details for final printing
        :return:
        """
        return 'Version: {0}, Version Date: {1}'.format(str(__version__), __version_date__)

    def find_cds_delay(self):
        """ Method to find the actual start of the translated sequence
            introduced to sort out non-coding exon problems """
        '''
        :param transcript: currently a relic of the LRG process (29-01-2015), designed to separate the
                           dictionary population process into distinct sections for each transcript
        '''
        for transcript in self.transcriptdict['transcripts'].keys():
            self.transcriptdict['transcripts'][transcript]['cds_offset'] = self.cds[0].location.start
            offset_total = 0
            offset = self.transcriptdict['transcripts'][transcript]['cds_offset']
            exon_list = self.transcriptdict['transcripts'][transcript]['list_of_exons']
            exon_list.sort(key=float)
            for exon in exon_list:
                g_start = self.transcriptdict['transcripts'][transcript]['exons'][exon]['genomic_start']
                g_stop = self.transcriptdict['transcripts'][transcript]['exons'][exon]['genomic_end']
                if offset > g_stop:
                    offset_total = offset_total + (g_stop - g_start)
                elif g_stop > offset > g_start:
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
        for alternative in self.transcriptdict['Alt transcripts']:
            transcript_name = alternative
            self.transcriptdict['transcripts'][transcript_name] = {}
            self.transcriptdict['transcripts'][transcript_name]['exons'] = {}
            selected_cds = cds[alternative-1]
            protein_sequence = selected_cds.qualifiers['translation'][0] + '* '
            self.transcriptdict['transcripts'][transcript_name]['protein_seq'] = protein_sequence
            self.transcriptdict['transcripts'][transcript_name]['protein_accession'] = selected_cds.qualifiers['protein_id'][0]
            self.transcriptdict['protein_accession'] = selected_cds.qualifiers['protein_id'][0]


    def get_nm(self, transcript):
        mrna = self.mrna[0]
        self.transcriptdict['transcripts'][transcript]['NM_number'] = mrna.qualifiers['transcript_id'][0]
        cds_feature = self.cds[transcript-1]
        self.transcriptdict['transcripts'][transcript]['NP_number'] = cds_feature.qualifiers['protein_id'][0]
        print self.transcriptdict['transcripts'][transcript]['NP_number']
        print self.transcriptdict['transcripts'][transcript]['NM_number']
        # print self.transcriptdict['NM_number']



    def get_exons(self, exons):
        """
        This function is supplied with the list of exon tagged blocks from the features section
        and populates the exons region of the dictionary with the exon number, coordinates, and
        sequence segments which define the exon
        """
        '''
        :param exons: a list of the exon objects from the GenBank features list
        '''
        for cds in self.transcriptdict['transcripts'].keys():
            self.transcriptdict['transcripts'][cds]['list_of_exons'] = []
            exon_count = 1
            for x in exons:
                # Some Genbank files do not feature explicitly numbered exons
                if 'number' in x.qualifiers:
                    exon_number = x.qualifiers['number'][0]
                else:
                    exon_number = str(exon_count)
                    exon_count += 1
                self.transcriptdict['transcripts'][cds]['exons'][exon_number] = {}
                self.transcriptdict['transcripts'][cds]['list_of_exons'].append(exon_number)
                location_feature = x.location
                self.transcriptdict['transcripts'][cds]['exons'][exon_number]['genomic_start'] = location_feature.start
                self.transcriptdict['transcripts'][cds]['exons'][exon_number]['genomic_end'] = location_feature.end
                sequence = self.transcriptdict['full genomic sequence'][location_feature.start:location_feature.end]
                if self.transcriptdict['pad'] != 0:
                    pad = self.transcriptdict['pad']
                    pad5 = self.transcriptdict['full genomic sequence'][
                        location_feature.start - pad:location_feature.start]
                    pad3 = self.transcriptdict['full genomic sequence'][
                        location_feature.end:location_feature.end + pad]
                    sequence = pad5.lower() + sequence + pad3.lower()
                self.transcriptdict['transcripts'][cds]['exons'][exon_number]['sequence'] = sequence

    def fill_and_find_features(self):
        dictionary = self.transcriptdict['input'][self.transcriptdict['refseqname']]
        self.transcriptdict['full genomic sequence'] = dictionary.seq
        features = dictionary.features
        for feature in features:
            # Multiple exons are expected
            if feature.type == 'exon':
                self.exons.append(feature)
            # A single CDS is ideal, may cause some confusion if multiple exist
            elif feature.type == 'CDS':
                self.cds.append(feature)
            elif feature.type == 'mRNA':
                self.mrna.append(feature)
        self.transcriptdict['genename'] = self.exons[0].qualifiers['gene'][0]
        return features

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
        features = self.fill_and_find_features()
        self.transcriptdict['Alt transcripts'] = range(1, len(self.cds)+1)


        # Sort through SeqFeatures to find the good stuff
        self.transcriptdict['genename'] = self.exons[0].qualifiers['gene'][0]

        self.get_protein(self.cds)
        self.get_exons(self.exons)
        self.find_cds_delay()
        for transcript in self.transcriptdict['transcripts']:
            self.get_nm(transcript)
        return self.transcriptdict
