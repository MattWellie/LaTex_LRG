import unittest
from reader import Reader
from LrgParser import LrgParser


class TestFixture(unittest.TestCase):

    def setUp(self):
        self.test_lrg = LrgParser('LRG_TEST.xml', 10)
        self.transcriptdict = self.test_lrg.run()
        self.test_reader = Reader(self.transcriptdict, 1, True)


    def test_reader_init(self):
        pass

    def test_choose_number_string_1(self):
        output, wait_value, cds_count, amino_acid_counter, post_protein_printer, intron_offset, intron_in_padding,intron_out = self.test_reader.decide_number_string_character('a', 0, 0, 0, 0, 0, 5, 0, 5)
        self.assertEqual(output, '.')
        self.assertEqual(wait_value, 0)
        self.assertEqual(intron_in_padding, 4)
        self.assertEqual(post_protein_printer, 0)

    def test_choose_number_string_1(self):
        output, wait_value, cds_count, amino_acid_counter, post_protein_printer, intron_offset, intron_in_padding,intron_out = self.test_reader.decide_number_string_character('a', 0, 0, 0, 0, 0, 5, 0, 5)
        self.assertEqual(output, '.')
        self.assertEqual(wait_value, 0)
        self.assertEqual(intron_in_padding, 4)
        self.assertEqual(post_protein_printer, 0)

    def test_choose_number_string_1(self):
        pass
        output, wait_value, cds_count, amino_acid_counter, post_protein_printer, intron_offset, intron_in_padding,intron_out = self.test_reader.decide_number_string_character('a', 0, 0, 0, 0, 0, 5, 0, 5)
        self.assertEqual(output, '.')
        self.assertEqual(wait_value, 0)
        self.assertEqual(intron_in_padding, 4)
        self.assertEqual(post_protein_printer, 0)