# To measure the length difference between the shortest and longest sequences in each of the 255,191 gene clusters with at least 100 cluster members. 

import sys
from Bio import SeqIO

cluster_multifasta = sys.argv[1]

seq_lens = [len(i.seq) for i in SeqIO.parse(cluster_multifasta,'fasta')]

max_len_diff = max(seq_lens) - min(seq_lens)

print(max_len_diff)
