import unittest
from GbkParser import GbkParser
#from latex_writer import LatexWriter

class TestFixture(unittest.TestCase):

    def setUp(self):
        self.test_gbk = GbkParser('input\\GB_TEST.gb', 10)

    def test_GbkParser(self):
        self.assertEqual(str(self.test_gbk.__class__), 'GbkParser.GbkParser')
        self.assertEqual(self.test_gbk.transcriptdict['pad'], 10)
        self.assertEqual(self.test_gbk.transcriptdict['pad_offset'], 0)
        self.assertEqual(self.test_gbk.is_matt_awesome, True)
        self.assertEqual(self.test_gbk.transcriptdict['filename'], 'input\\GB_TEST_10')
        # self.assertRaises(IOError, GbkParser('notatest.gb', -1))

    def test_fill_and_find_features(self):
        """This test should pass based on the GB_TEST.gb file 9/2/2015"""
        features = self.test_gbk.fill_and_find_features()
        self.test_gbk.transcriptdict['Alt transcripts'] = range(1, len(self.test_gbk.cds)+1)
        self.test_gbk.transcriptdict['genename'] = self.test_gbk.exons[0].qualifiers['gene'][0]
        self.assertAlmostEqual(str(self.test_gbk.transcriptdict['full genomic sequence'][0:60]), 'GAAAAGAAAAGAAAAGAAAAGAAAAGAAAAGAAAAGAAAAGAAAAGAAAAGAAAAGAAAA')
        self.assertEqual(len(features), 10)
        self.assertEqual(self.test_gbk.transcriptdict['genename'], 'WELLAND')
        self.assertEqual(len(self.test_gbk.cds), 1)

    #
    # def test_grab_element_fail(self):
    #     """This test should fail, as it references a non-existent node"""
    #     print 'Next String should be a failure:'
    #     element = self.test_gbk.grab_element('fixed_annotation/failure')
    #     self.assertEqual(str(element.__class__),  "<type 'NoneType'>")
    #     self.assertEqual(element, None)

    def test_get_protein(self):
        features = self.test_gbk.fill_and_find_features()
        self.test_gbk.transcriptdict['Alt transcripts'] = range(1, len(self.test_gbk.cds)+1)
        self.test_gbk.transcriptdict['genename'] = self.test_gbk.exons[0].qualifiers['gene'][0]
        self.test_gbk.get_protein(self.test_gbk.cds)
        self.test_gbk.get_protein(self.test_gbk.cds)
        self.assertEqual(self.test_gbk.transcriptdict['transcripts'][1]['protein_seq'], 'ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLM* ')

    def test_get_exons1(self):
        features = self.test_gbk.fill_and_find_features()
        self.test_gbk.transcriptdict['Alt transcripts'] = range(1, len(self.test_gbk.cds)+1)
        self.test_gbk.transcriptdict['genename'] = self.test_gbk.exons[0].qualifiers['gene'][0]
        self.test_gbk.get_protein(self.test_gbk.cds)
        self.test_gbk.get_exons(self.test_gbk.exons)
        # print self.test_gbk.transcriptdict['transcripts'].keys()
        self.test_gbk.transcriptdict['transcripts'][1]['list_of_exons'].sort(key=float)
        exons = self.test_gbk.transcriptdict['transcripts'][1]["exons"]
        exon_keys = exons.keys()
        exon_keys.sort()
        self.assertEqual(exons.keys(), ['1', '3', '2'])
        self.assertEqual(self.test_gbk.transcriptdict['transcripts'][1]["list_of_exons"], ['1', '2', '3'])
        self.assertEqual(exon_keys, self.test_gbk.transcriptdict['transcripts'][1]["list_of_exons"])
        self.assertEqual(self.test_gbk.transcriptdict['transcripts'][1]['exons']['1']['genomic_start'], 800)
        self.assertEqual(self.test_gbk.transcriptdict['transcripts'][1]['exons']['1']['genomic_end'], 1020)
        self.assertEqual(self.test_gbk.transcriptdict['transcripts'][1]['exons']['2']['genomic_start'], 1620)
        self.assertEqual(self.test_gbk.transcriptdict['transcripts'][1]['exons']['2']['genomic_end'], 1779)
        self.assertEqual(self.test_gbk.transcriptdict['transcripts'][1]['exons']['3']['genomic_start'], 2379)
        self.assertEqual(self.test_gbk.transcriptdict['transcripts'][1]['exons']['3']['genomic_end'], 2655)
        for value in exon_keys:
            if value not in ['1', '2', '3']:
                print 'Unexpected exon identified, process failed'
                exit()

    def test_get_exons2(self):
        features = self.test_gbk.fill_and_find_features()
        self.test_gbk.transcriptdict['Alt transcripts'] = range(1, len(self.test_gbk.cds)+1)
        self.test_gbk.transcriptdict['genename'] = self.test_gbk.exons[0].qualifiers['gene'][0]
        self.test_gbk.get_protein(self.test_gbk.cds)
        self.test_gbk.get_exons(self.test_gbk.exons)
        self.assertEqual(str(self.test_gbk.transcriptdict['transcripts'][1]['exons']['1']['sequence']), 'gaaaagaaaaACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTaaaagaaaag')
        self.assertEqual(str(self.test_gbk.transcriptdict['transcripts'][1]['exons']['2']['sequence']), 'gaaaagaaaaACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTATGACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTaaaagaaaag')
        self.assertEqual(str(self.test_gbk.transcriptdict['transcripts'][1]['exons']['3']['sequence']), 'gaaaagaaaaACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTATAAACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTaaaagaaaag')

    def test_find_cds_delay(self):
        features = self.test_gbk.fill_and_find_features()
        self.test_gbk.transcriptdict['Alt transcripts'] = range(1, len(self.test_gbk.cds)+1)
        self.test_gbk.transcriptdict['genename'] = self.test_gbk.exons[0].qualifiers['gene'][0]
        self.test_gbk.get_protein(self.test_gbk.cds)
        self.test_gbk.get_exons(self.test_gbk.exons)
        self.test_gbk.transcriptdict['transcripts'][1]['cds_offset'] = self.test_gbk.cds[0].location.start
        self.assertEqual(1676, self.test_gbk.transcriptdict['transcripts'][1]['cds_offset'])
        self.test_gbk.find_cds_delay()
        self.assertEqual(276, self.test_gbk.transcriptdict['transcripts'][1]['cds_offset'])

if __name__ == '__main__':
    unittest.main()
