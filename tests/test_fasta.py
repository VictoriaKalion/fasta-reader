import unittest
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from fasta_reader import Seq, FastaReader


class TestSeq(unittest.TestCase):
    def test_seq_creation(self):
        seq = Seq("test_header", "ATCG")
        self.assertEqual(seq.header, "test_header")
        self.assertEqual(seq.sequence, "ATCG")

    def test_seq_length(self):
        seq = Seq("test", "ATCGATCG")
        self.assertEqual(len(seq), 8)

    def test_alphabet_detection(self):
        nuc_seq = Seq("nuc", "ATCGATCG")
        prot_seq = Seq("prot", "MKTVETFKL")

        self.assertEqual(nuc_seq.get_alphabet(), 'nucleotide')
        self.assertEqual(prot_seq.get_alphabet(), 'protein')


class TestFastaReader(unittest.TestCase):
    def setUp(self):
        # Создаем тестовый FASTA файл
        self.test_fasta = ">test_seq1\nATCG\n>test_seq2\nGCTA\n"
        with open('test_file.fasta', 'w') as f:
            f.write(self.test_fasta)

    def test_valid_fasta(self):
        reader = FastaReader('test_file.fasta')
        self.assertTrue(reader.is_valid_fasta())

    def test_sequence_reading(self):
        reader = FastaReader('test_file.fasta')
        sequences = list(reader.read_sequences())

        self.assertEqual(len(sequences), 2)
        self.assertEqual(sequences[0].header, 'test_seq1')


if __name__ == '__main__':
    unittest.main()