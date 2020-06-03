import sys
import random

'''
Reads the pairwise counts file and generates a matrix
'''

species = set()
pairwise_counts = {}

with open(sys.argv[1],'r') as f:
	for line in f:
		attrs = line.strip().split('\t')
		if line[0] == '#':
			continue
		species.add(attrs[0])
    		species.add(attrs[1])
    		if attrs[0] not in pairwise_counts:
			pairwise_counts[attrs[0]] = {}
		if attrs[1] not in pairwise_counts:
			pairwise_counts[attrs[1]] = {}
		pairwise_counts[attrs[0]][attrs[1]] = int(attrs[2])
    		pairwise_counts[attrs[1]][attrs[1]] = int(attrs[2])

species = list(species)

line = ""
for i in xrange(0,len(species)):
	line += species[i]
	line += '\t'

print line
for i  in xrange(0,len(species)):
	line = ""
	line += species[i]+'\t'
	for j in xrange(0,len(species)):
	    if species[j] in pairwise_counts[species[i]]:
	    	line += str(pairwise_counts[species[i]][species[j]])+'\t'
	    else:
	    	num = random.choice([1,2,4,3])
	    	line += str(num)+'\t'
	print line
