import unittest
from LrgParser import LrgParser
from GbkParser import GbkParser
from reader import Reader
from latex_writer import LatexWriter

class TestFixture(unittest.TestCase):

	def setUp(self):
		self.test_lrg = LrgParser('LRG_TEST.xml', 10)

	def test_LrgParser(self):
		#test_lrg = LrgParser('LRG_TEST.xml', 10)
		self.assertEqual(str(self.test_lrg.__class__), 'LrgParser.LrgParser')

	def test_grab_element(self):
		element = self.test_lrg.grab_element('fixed_annotation/sequences')
		self.assertEqual(str(element.__class__), "<type 'str'>")
		self.assertEqual(element[0:60], 'GAAAAGAAAAGAAAAGAAAAGAAAAGAAAAGAAAAGAAAAGAAAAGAAAAGAAAAGAAAA')


if __name__ == '__main__':
	unittest.main()
