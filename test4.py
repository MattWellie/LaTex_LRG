import unittest
from LrgParser import LrgParser
from reader import Reader
from latex_writer import LatexWriter

class TestFixture(unittest.TestCase):
    """
    This class must be dealt with separately during testing
    Directory navigation causes a fault when searching for test input file

    in PyCharm highlight commented section and press left Ctrl + / to uncomment
    """

    def setUp(self):
        self.test_lrg = LrgParser('LRG_TEST.xml', 10)
        self.test_lrg.run()
        self.test_reader = Reader(self.test_lrg.transcriptdict, 1, True)
        self.output_list = self.test_reader.run()
    #     self.test_latex = LatexWriter(self.output_list, self.test_lrg.transcriptdict['filename'])
    #     self.latex_name = self.test_latex.run()
    #     print self.latex_name
    #
    # def test_things(self):
    #     self.assertEqual(str(self.latex_name.__class__), "<type 'str'>")