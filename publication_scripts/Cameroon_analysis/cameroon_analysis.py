import argparse
from Bio import SeqIO
from collections import Counter

# python analyze_cameroon.py -fastq ERR2619707.fastq -genes PROKKA_07052019.ffn -clustered clustered2IGC.blast -sam_pred_genes_nc ERR2619707.all_genes.sam -sam_pred_genes_cord ERR2619707.all_genes.concordant.sam -sam_igc_nc ERR2619707.igc.sam -sam_igc_cord ERR2619707.igc.concordant.sam

parser = argparse.ArgumentParser()
parser.add_argument("-fastq", help="fastq file of Cameroon raw reads i.e. ERR2619707.fastq")
parser.add_argument("-genes", help="fasta file of predicted genes i.e. cameroon_predicted_genes.fasta")
parser.add_argument("-clustered", help="file of predicted genes assigned to IGC clusters i.e. clustered2IGC.blast")
parser.add_argument("-sam_pred_genes_nc", help="sam file (not requiring concordant mappings) for reads mapped to predicted genes i.e. ERR2619707.all_genes.sam")
parser.add_argument("-sam_pred_genes_cord", help="sam file (requiring concordant mappings) for reads mapped to predicted genes i.e. ERR2619707.all_genes.concordant.sam")
parser.add_argument("-sam_igc_nc", help="sam file (not requiring concordant mappings) for reads mapped to IGC i.e. ERR2619707.igc.sam")
parser.add_argument("-sam_igc_cord", help="sam file (requiring concordant mappings) for reads mapped to IGC i.e. ERR2619707.igc.concordant.sam")
args = parser.parse_args()


# fastqs = {str(i.id) for i in SeqIO.parse(args.fastq,'fastq')}
# print("Total number of reads: ",len(fastqs))

# predicted_genes = {str(i.id) for i in SeqIO.parse(args.genes,'fasta')}
# print("Total number of predicted genes: ",len(predicted_genes))

predicted_clustered_genes = {i.strip().split('\t')[0] for i in open(args.clustered)}
print("Total number of predicted genes assigned to IGC clusters: ",len(predicted_clustered_genes))

IGC_clustered_assigned_predicted_genes = {i.strip().split('\t')[1] for i in open(args.clustered)}
print("Total number of IGC clusters assigned to predicted genes: ",len(IGC_clustered_assigned_predicted_genes))

total_num_reads = 49399939.0

print('''\n ####### Read mapping to predicted genes analysis: non-concordant ############# ''')
reads = []
genes = []
flags = []

for i in open(args.sam_pred_genes_nc):
	if i[0] != '@':
		tmp = i.strip().split('\t')
		read = tmp[0]
		flag = tmp[1]
		gene = tmp[2]
		flags.append(flag)
		reads.append(read)
		genes.append(gene)


print("Total number reads mapped to predicted genes (concordant mappings not required): ",len(reads),len(reads)/total_num_reads)
# print(len(set(reads)))
print("Total number of predicted genes that reads mapped to (concordant mappings not required): ",len(set(genes)))


print('Sam file flag counts:')
for k,v in Counter(flags).items():
	print(k,v)

print('''\n ####### Read mapping to IGC analysis: non-concordant ############# ''')
reads = []
genes = []
flags = []

for i in open(args.sam_igc_nc):
	if i[0] != '@':
		tmp = i.strip().split('\t')
		read = tmp[0]
		flag = tmp[1]
		gene = tmp[2]
		flags.append(flag)
		reads.append(read)
		genes.append(gene)

print("Number reads mapped to IGC genes: ",len(reads),len(reads)/total_num_reads)
# print(len(set(reads)))
print("Number IGC clusters that reads mapped to : ",len(set(genes)))

print('Sam file flag counts:')
for k,v in Counter(flags).items():
	print(k,v)


print('''\n ####### Concordant read-mapping analysis ########################### ''')

pred_genes_c = args.sam_pred_genes_cord
igc_c = args.sam_igc_cord

PGC_reads = {'cpg':[],'ucpg':[]}
clustered_reads = {}
unclustered_reads = {}
for i in open(pred_genes_c):
	tmp = i.strip().split('\t')
	read = tmp[0]
	gene = tmp[2]
	if gene in predicted_clustered_genes:
		PGC_reads['cpg'].append(gene)
		clustered_reads[read] = 0
	else:
		PGC_reads['ucpg'].append(gene)
		unclustered_reads[read] = 0

clustered_genes = set(PGC_reads['cpg'])
unclustered_genes = set(PGC_reads['ucpg'])

IGCC_reads = {'cpg':[],'other':[],'ucpg':[]}
for i in open(igc_c):
	tmp = i.strip().split('\t')
	read = tmp[0]
	gene = tmp[2]
	if read in clustered_reads:
		if gene in IGC_clustered_assigned_predicted_genes:
			IGCC_reads['cpg'].append(gene)
		else:
			IGCC_reads['other'].append(gene)
	elif read in unclustered_reads:
		IGCC_reads['ucpg'].append(gene)

total_num_reads

print("Reads mapped to IGC clusters corresponding to clustered predicted genes: ",len(IGCC_reads['cpg']),len(IGCC_reads['cpg'])/total_num_reads)
print("Number of IGC clusters corresponding to clustered predicted genes with mapped reads: ",len(set(IGCC_reads['cpg'])),len(set(IGCC_reads['cpg'])))
print("Reads mapped to clustered predicted genes and genes other than corresponding IGC genes: ",len(IGCC_reads['other']),len(IGCC_reads['other'])/total_num_reads)
print("Number of IGC clusters with mapped reads from clustered predicted genes but not corresponding IGC genes: ",len(set(IGCC_reads['other'])),len(set(IGCC_reads['other'])))
print("Reads mapped to IGC clusters and unclustered predicted genes: ",len(IGCC_reads['ucpg']),len(IGCC_reads['ucpg'])/total_num_reads)
print("Number of IGC clusters with mapped reads from unclustered predicted genes: ",len(set(IGCC_reads['ucpg'])),len(set(IGCC_reads['ucpg'])))
