import sys

clstr = sys.argv[1]

def parse_clstr(x,out):
	mems = []
	for i in open(x):
		if i[0] == ">":
			if mems != []:
				print('<50\n')
				return None
			else: continue
		else:
			if i.split('... ')[1].strip() == '*':
				mems.append(100.0)
			else:
				pident = float(i.strip().split('/')[-1].split('%')[0])
				mems.append(pident)
	if mems != []:
		print(min(mems)


parse_clstr(clstr,out)









