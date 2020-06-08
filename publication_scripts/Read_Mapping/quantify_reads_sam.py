import os,sys

# Read Sam files from Bowtie2 or BWA mapping result
f = sys.argv[1] 

unmapped,genes,read_count,unique,multi = 0,{},{},0,0

for i in open(f):
	if i.startswith('@'):
		continue
	tmp = i.strip().split('\t')
	if tmp[1] in ['4','2048','2064']:
		unmapped += 1
		continue
	genes[tmp[2]]=0			
	if tmp[0] in read_count:
		read_count[tmp[0]] += 1
	else:
		read_count[tmp[0]] = 1

for k,v in read_count.items():
	if v > 1:
		multi += 1
	elif v == 1:
		unique += 1

with open('results_counting.txt','a') as out:
	out.write(f+'\t'+str(len(genes))+'\t'+str(unmapped)+'\t'+str(unique)+'\t'+str(multi)+'\n')



