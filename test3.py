import unittest
from reader import Reader
from LrgParser import LrgParser


class TestFixture(unittest.TestCase):

    def setUp(self):
        self.test_lrg = LrgParser('LRG_TEST.xml', 10)
        self.transcriptdict = self.test_lrg.run()
        self.test_reader = Reader(self.transcriptdict, 1, True)
        self.protein = self.transcriptdict['transcripts'][1]['protein_seq']

    """
    This section evalutes the performance of the decide_number_string_char
    method of the reader class.
    input params:
        char: next base of input
        wait_value: variable indicating if a number has already been written
        cds_count: the CDS position of the current char/base
        amino_acid_counter: position of the amino acid in the protein sequence
        post_protein_printer: to indicate the position of the exon after stop codon
        intron_offset:
        intron_in_padding:
        protein_length: length of protein sequence
        intron_out:

        return: all input values complete with appropriate additions and subtractions, and
                 the new character(s) to be added to the number string
    """
    def test_choose_number_string1(self):
        output, wait_value, cds_count, amino_acid_counter, post_protein_printer, intron_offset, intron_in_padding,intron_out = self.test_reader.decide_number_string_character('a', 0, 0, 0, 0, 0, 5, 0, 5)
        self.assertEqual(output, '.')
        self.assertEqual(wait_value, 0)
        self.assertEqual(intron_in_padding, 4)
        self.assertEqual(post_protein_printer, 0)

    def test_choose_number_string2(self):
        output, wait_value, cds_count, amino_acid_counter, post_protein_printer, intron_offset, intron_in_padding,intron_out = self.test_reader.decide_number_string_character('A', 0, 101, 21, 0, 0, 0, 400, 0)
        self.assertEqual(output, '|101')
        self.assertEqual(wait_value, 3)
        self.assertEqual(intron_in_padding, 0)
        self.assertEqual(post_protein_printer, 0)

    def test_choose_number_string3(self):
        output, wait_value, cds_count, amino_acid_counter, post_protein_printer, intron_offset, intron_in_padding,intron_out = self.test_reader.decide_number_string_character('A', 0, 100, 21, 0, 0, 0, 5, 0)
        self.assertEqual(output, '|+1')
        self.assertEqual(wait_value, 2)
        self.assertEqual(intron_in_padding, 0)
        self.assertEqual(post_protein_printer, 1)

    """
    Methods testing the decide_amino_string_character function of reader
    """

    def test_decide_amino_string1(self):
        # lower case, c_c = 1, aa_c = 0, c_num = False                                                    char, c_count, aa_count, c_numbered, protein
        output, codon_count, amino_acid_counter, codon_numbered = self.test_reader.decide_amino_string_character('a', 1, 0, False, self.protein)
        self.assertEqual(output, ' ')

    def test_decide_amino_string2(self):
        # upper case, c_c = 1, aa_c = 0, c_num = False
        output, codon_count, amino_acid_counter, codon_numbered = self.test_reader.decide_amino_string_character('A', 1, 0, False, self.protein)
        self.assertEqual(output, ' ')

    def test_decide_amino_string3(self):
        # upper case, c_c = 1, aa_c = 0, c_num = False
        self.test_reader.amino_printing = True
        output, codon_count, amino_acid_counter, codon_numbered = self.test_reader.decide_amino_string_character('A', 3, 14, False, self.protein)
        self.assertEqual(output, 'O')

    def test_decide_amino_string4(self):
        self.test_reader.amino_printing = True
        output, codon_count, amino_acid_counter, codon_numbered = self.test_reader.decide_amino_string_character('A', 1, 15, False, self.protein)
        self.assertEqual(output, ' ')

    def test_decide_amino_string5(self):
        self.test_reader.amino_printing = True
        output, codon_count, amino_acid_counter, codon_numbered = self.test_reader.decide_amino_string_character('A', 3, 15, False, self.protein)
        self.assertEqual(output, 'P')

    def test_decide_amino_number_string_character(self):
        pass
        output, amino_wait, codon_numbered, amino_acid_counter = self.test_reader.decide_amino_string_character('a', 1, 10, True, self.protein)
        self.assertEqual(output, ' ')