lines=open('logs.txt','r').read().split('\n')
# sensi 1.00 speci 0.77

best_speci=0
for line in lines:
	if 'sensi 1.00' in line:
		elts=line.split()
		sensi=elts[1]
		speci=elts[3]
		if float(speci)>best_speci:
			best_speci=float(speci)
print (best_speci)