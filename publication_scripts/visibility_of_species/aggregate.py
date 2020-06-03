import sys

total_hidden = {}

count_map = {}


with open(sys.argv[1],'r') as f:
	for line in f:
		if line[0] == '#':
			continue
		attrs = line.strip().split('\t')
		species = attrs[1]
		hidden = int(attrs[2])
    		total = int(attrs[-1])
    		genus_species = attrs[1].split(' ')[0]
		genus_hidden = attrs[0].split(' ')[0]
    		ratio = hidden*1.0/total
		#if genus_species == genus_hidden:
		#	continue
		if species not in total_hidden:
			total_hidden[species] = 0
		total_hidden[species] += ratio
		if species not in count_map:
			count_map[species] = []
		count_map[species].append([attrs[0],hidden])


sorted_species = sorted(total_hidden.items(),key=lambda x:x[1],reverse=True)


for i in xrange(0,len(sorted_species)):
	hidden_species = sorted_species[i][0]
	for each in count_map[hidden_species]:
		if hidden_species != each[0]:
			print hidden_species+'\t'+each[0]+'\t'+str(each[1])
