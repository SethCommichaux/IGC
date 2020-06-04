import sys

diamond_results = sys.argv[1]

# collect number of gene sequences in IGC cluster being analyzed
gene_counts = len({k.strip().split('\t')[0]:0 for k in open(diamond_results)})
cover_set = {}

# map species labels from nr database hits to cluster sequences
for j in open(diamond_results):
	tmp = j.strip().split('\t')
	gene = tmp[0]
	taxa = tmp[-1].split('[')[-1].split(']')[0]
	if len(taxa.split(' ')) == 1: continue # ignore taxonomic labels without species labels
	if taxa not in cover_set:
		cover_set[taxa] = {gene:0}
	else:
		cover_set[taxa][gene] = 0  

results,c,ambiguous,candidates = [],0,0,[]

# approximate set cover of species in a greedy fashion
for k,v in reversed(sorted(cover_set.items(),key=lambda x:len(x[1]))):
	results += v.keys()
	c += 1
	candidates.append(k)
	if len(set(results)) >= gene_counts:
		print(diamond_results,candidates,c,True)
		break
else:
	print(diamond_results,candidates,False)

