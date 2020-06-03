import sys

clstr = sys.argv[1]

def parse_clstr(x,out):
	mems = []
	for i in open(x):
		if i[0] == ">":
			if mems != []:
				out.write(str(min(mems))+'\n')
				mems = []
		else:
			if i.split('... ')[1].strip() == '*':
				continue
			else:
				pident = i.strip().split('/')[-1].split('%')[0]
				mems.append(pident)
	if mems != []:
		out.write(str(min(mems))+'\n')


with open('min_clstr.txt','w') as out:
	parse_clstr(clstr,out)









