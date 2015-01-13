from Bio import SeqIO
import sys

filename = sys.argv[1]
genome=SeqIO.read(filename,'genbank') #you MUST tell SeqIO what format is being read
print genome.features