import unittest
from GbkParser import GbkParser
#from reader import Reader
#from latex_writer import LatexWriter

class TestFixture(unittest.TestCase):

    def setUp(self):
        self.test_gbk = GbkParser('GB_TEST.gb', 10)

    def test_GbkParser(self):
        self.assertEqual(str(self.test_gbk.__class__), 'GbkParser.GbkParser')

    def test_grab_element(self):
        """This test should pass based on the LRG_TEST.xml file 3/2/2015"""
        element = self.test_gbk.grab_element('fixed_annotation/sequence')
        self.assertEqual(str(element.__class__), "<type 'str'>")
        self.assertEqual(element[0:60], 'gaaaagaaaagaaaagaaaagaaaagaaaagaaaagaaaagaaaagaaaagaaaagaaaa')
    
    def test_grab_element_fail(self):
        """This test should fail, as it references a non-existent node"""
        print 'Next String should be a failure:'
        element = self.test_gbk.grab_element('fixed_annotation/failure')
        self.assertEqual(str(element.__class__),  "<type 'NoneType'>")
        self.assertEqual(element, None)

    def test_get_exon_coords(self):
        self.test_gbk.get_exon_coords()
        self.test_gbk.transcriptdict['transcripts'][1]['list_of_exons'].sort(key=float)
        exons = self.test_gbk.transcriptdict['transcripts'][1]["exons"]
        #print 'These are the exon keys: ' + str(exons.keys())
        exon_keys = exons.keys()
        exon_keys.sort()
        #print 'These are the sorted exon keys: ' + str(exon_keys)
        self.assertEqual(exons.keys(), ['1', '3', '2'])
        self.assertEqual(self.test_gbk.transcriptdict['transcripts'][1]["list_of_exons"], ['1', '2', '3'])
        self.assertEqual(exon_keys, self.test_gbk.transcriptdict['transcripts'][1]["list_of_exons"])
        self.assertEqual(self.test_gbk.transcriptdict['transcripts'][1]['exons']['1']['genomic_start'], 801)
        self.assertEqual(self.test_gbk.transcriptdict['transcripts'][1]['exons']['1']['genomic_end'], 1020)
        self.assertEqual(self.test_gbk.transcriptdict['transcripts'][1]['exons']['2']['genomic_start'], 1621)
        self.assertEqual(self.test_gbk.transcriptdict['transcripts'][1]['exons']['2']['genomic_end'], 1779)
        self.assertEqual(self.test_gbk.transcriptdict['transcripts'][1]['exons']['3']['genomic_start'], 2380)
        self.assertEqual(self.test_gbk.transcriptdict['transcripts'][1]['exons']['3']['genomic_end'], 2655)
        for value in exon_keys:
            if value not in ['1', '2', '3']:
                print 'Unexpected exon identified, process failed'
                exit()

    def test_grab_exon_contents(self):
        self.test_gbk.get_exon_coords()
        self.test_gbk.grab_exon_contents(self.test_gbk.grab_element('fixed_annotation/sequence'))
        transcripts = self.test_gbk.transcriptdict['transcripts'].keys()
        self.assertEqual(self.test_gbk.transcriptdict['transcripts'][1]['exons']['1']['sequence'], 'gaaaagaaaaACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTaaaagaaaaga')
        self.assertEqual(self.test_gbk.transcriptdict['transcripts'][1]['exons']['2']['sequence'], 'gaaaagaaaaACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTATGACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTaaaagaaaaga')
        self.assertEqual(self.test_gbk.transcriptdict['transcripts'][1]['exons']['3']['sequence'], 'gaaaagaaaaACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTATAAACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTaaaagaaaaga')

    def test_gt_protein_exons(self):
        self.test_gbk.get_exon_coords()
        self.test_gbk.grab_exon_contents(self.test_gbk.grab_element('fixed_annotation/sequence'))
        self.test_gbk.get_protein_exons()
        self.assertEqual(self.test_gbk.transcriptdict['transcripts'][1]['protein_seq'], 'ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLM* ')

    def test_find_cds_delay(self):
        self.test_gbk.get_exon_coords()
        self.test_gbk.grab_exon_contents(self.test_gbk.grab_element('fixed_annotation/sequence'))
        self.test_gbk.get_protein_exons()
        self.assertEqual(1677, self.test_gbk.transcriptdict['transcripts'][1]['cds_offset'])#
        self.test_gbk.find_cds_delay(1)
        self.assertEqual(276, self.test_gbk.transcriptdict['transcripts'][1]['cds_offset'])#

if __name__ == '__main__':
    unittest.main()
