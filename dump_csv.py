import os
import math
import numpy as np
import matplotlib.pyplot as plt

vals=[]
results=[0,0]
for dd in ['../kenya_files/']:
	fs=sorted(os.listdir(dd))

	for i in fs:
		if 'summary' in i:
			f=open(dd+'/'+i).read()
			lines=f.split('\n')
			elts0=lines[0].split(',')
			elts1=lines[1].split(',')
			# idx=0
			# for j in range(len(elts0)):
			# 	print (idx,elts0[j],elts1[j])
			# 	idx+=1
			signal=elts1[53:57]
			noise=elts1[57:61]
			snrs=elts1[61:65]
			cfit=elts1[81]
			# snrs=[i if i != 'NaN' else '0' for i in snrs ]
			# signal=[i if i != 'NaN' else '0' for i in signal ]
			# noise=[i if i != 'NaN' else '0' for i in noise ]
			thresh=10
			freq=2
			count=0
			for k in snrs:
				if k=='NaN':
					continue
				if math.ceil(float(k))>=thresh:
					count+=1
			result='Refer'
			if count>=freq:
				result='Pass'
				results[1]+=1
			else:
				results[0]+=1
			# print ("%s %d %d %d %d"%(i,math.ceil(float(signal[0])),math.ceil(float(signal[1])),math.ceil(float(signal[2])),math.ceil(float(signal[3]))))
			# print ("%s %d %d %d %d"%(i,math.ceil(float(noise[0])),math.ceil(float(noise[1])),math.ceil(float(noise[2])),math.ceil(float(noise[3]))))
			snrs2=[str(math.ceil(float(k)))  if k != 'NaN' else str(k) for k in snrs]
			# if result=='Pass':
			print ("%s %s %s %s %s %s %s"%(i,snrs2[0],snrs2[1],snrs2[2],snrs2[3],result,cfit))
				# vals.append(np.mean(snrs2))
			# print (f)
			# break
print (thresh,freq,results)

# plt.figure()
# plt.hist(vals)
# plt.show()



