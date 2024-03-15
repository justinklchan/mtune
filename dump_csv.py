import os
import math
import numpy as np
import matplotlib.pyplot as plt

noises=[]
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
			noise=[int(float(i)) if i != 'NaN' else 150 for i in noise ]
			noise=[i if i !=0 else 150 for i in noise]
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
			snrs2=[(math.ceil(float(k))) if k != 'NaN' else 0 for k in snrs]
			
			threshs=[7,7,11,12]
			band=2
			# threshs=[6,6,11,10]
			# band=3
			# threshs=[6,11,6,11]
			# band=2
			counter=0
			for k in range(4):
				if snrs2[k]>=threshs[k]:
					counter+=1
			if counter>=band:
				result2='Pass'
			else:
				result2='Refer'
			if '150-Name-right' in i or '201' in i or '351-Name-left' in i:
			# 	print (noise)
			# if noise[0]<=64 or noise[1]<=60 or noise[2]<=53 or noise[3]<=50:
				print ("%s %d %d %d %d %s %s %s"%(i,snrs2[0],snrs2[1],snrs2[2],snrs2[3],result,result2,cfit))
				print (noise)
			noises.append(noise)
				# vals.append(np.mean(snrs2))
			# print (f)
			# break
print (thresh,freq,results)
print (threshs)
# plt.figure()
# plt.hist(vals)
# plt.show()
noises=np.asarray(noises)
print (np.min(noises[:,0]))
print (np.min(noises[:,1]))
print (np.min(noises[:,2]))
print (np.min(noises[:,3]))

# plt.figure()
# plt.hist(noises[:,0])
# plt.hist(noises[:,1])
# plt.hist(noises[:,2])
# plt.hist(noises[:,3])
# plt.show()
