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


if __name__ == '__main__':
    unittest.main()
