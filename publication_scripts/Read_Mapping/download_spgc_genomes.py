import os
import sys

ftp = {}
with open('assembly_summary_refseq.txt') as f:
    for line in f:
        if line.startswith('#'):
            continue
        val = line.strip().split('\t')
        ftp[val[5]] = val[19]
        # print val[19], val[5]

ftp_hist = {}
with open('assembly_summary_refseq_historical.txt') as f:
    for line in f:
        if line.startswith('#'):
            continue
        val = line.strip().split('\t')
        ftp_hist[val[5]] = val[19]

with open('supp_spgc_genomes_tab.txt') as f:
    for line in f:
        if line.startswith('#'):
            continue
        l = line.strip().split('\t')
        # print l
        taxon_id = l[0]
# 
        if l[-1] == '1':
            if l[0] in ftp:
                print '\t'.join([l[0], ftp[l[0]], "new"])
            elif l[0] in ftp_hist:
                print '\t'.join([l[0], ftp_hist[l[0]], "old"])
            else:
                print '\t'.join([l[0], "NA", "NA"])




