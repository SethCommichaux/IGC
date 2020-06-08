import sys,os
# Read in SAM file
f = sys.argv[1]

gene_lengths = {i.strip().split('\t')[0]:int(i.strip().split('\t')[1]) for i in open('IGC.fa.fai')}

gene_count = {}
for i in open(f):
	if i.startswith('@'):
		continue
	tmp = i.strip().split('\t')
	if tmp[1] in ['4','2048','2064']:
		continue
	if tmp[2] in gene_count:
		gene_count[tmp[2]][0] += 1
	else:
		gene_count[tmp[2]] = [1,0]

for k,v in gene_count.items():
	gene_count[k][1] = float(v[0])/gene_lengths[k]

total = float(sum([v[1] for v in gene_count.values()]))

with open(f+'.gene.counts','w') as out:
	out.write('Gene\tRaw_count\tbi\trel_abundance\n')
	for k,v in gene_count.items():
		out.write(str(k)+'\t'+str(v[0])+'\t'+str(v[1])+'\t'+str(v[1]/total)+'\n')



