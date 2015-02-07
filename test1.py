import unittest
from LrgParser import LrgParser
#from GbkParser import GbkParser
#from reader import Reader
#from latex_writer import LatexWriter

class TestFixture(unittest.TestCase):

    def setUp(self):
        self.test_lrg = LrgParser('LRG_TEST.xml', 10)

    def test_LrgParser(self):
        self.assertEqual(str(self.test_lrg.__class__), 'LrgParser.LrgParser')

    def test_grab_element(self):
        """This test should pass based on the LRG_TEST.xml file 3/2/2015"""
        element = self.test_lrg.grab_element('fixed_annotation/sequence')
        self.assertEqual(str(element.__class__), "<type 'str'>")
        self.assertEqual(element[0:60], 'GAAAAGAAAAGAAAAGAAAAGAAAAGAAAAGAAAAGAAAAGAAAAGAAAAGAAAAGAAAA')
    
    def test_grab_element_fail(self):
        """This test should fail, as it references a non-existent node"""
        element = self.test_lrg.grab_element('fixed_annotation/failure')
        self.assertEqual(str(element.__class__),  "<type 'NoneType'>")
        self.assertEqual(element, None)

    def test_get_exon_coords(self):
        self.test_lrg.get_exon_coords()
        # print 'exon list = ' + 
        self.test_lrg.transcriptdict['transcripts'][1]['list_of_exons'].sort(key=float)
        exons = self.test_lrg.transcriptdict['transcripts'][1]["exons"]
        #print 'These are the exon keys: ' + str(exons.keys())
        exon_keys = exons.keys()
        exon_keys.sort()
        #print 'These are the sorted exon keys: ' + str(exon_keys)
        self.assertEqual(exons.keys(), ['1', '3', '2'])
        self.assertEqual(self.test_lrg.transcriptdict['transcripts'][1]["list_of_exons"], ['1', '2', '3'])
        self.assertEqual(exon_keys, self.test_lrg.transcriptdict['transcripts'][1]["list_of_exons"])

    def test_grab_exon_contents(self):
        pass

    def test_gt_protein_exons(self):
        pass

    def test_find_cds_delay(self):
        pass


if __name__ == '__main__':
    unittest.main()
