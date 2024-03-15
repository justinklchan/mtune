import os
import re
import math
import numpy as np
from sklearn.metrics import confusion_matrix
import sys
import matplotlib.pyplot as plt
import itertools

# fname='MTUNEPractice-ConventionalVSSmartp_DATA_2024-03-03_2234'
# fname='MTUNEPractice-ConventionalVSSmartp_DATA_2024-03-07_0840'
fname='MTUNEPractice-ConventionalVSSmartp_DATA_2024-03-14_0802'
lines=open('../'+fname+'.csv').read().split('\n')

result_code={
	'3':'Incomplete',
	'2':'Refer',
	'1':'Pass',
	'':''
}
site_code={
	'1':'KNH',
	'2':'Mathare',
}

fs=sorted(os.listdir('../kenya_files'))

def find_file(fname):
	for i in fs:
		if len(re.findall(fname, i))>0 and 'summary' in i:
			return i
	return ''

def parse_summary(fname,f,con,snr_thresh1,snr_thresh2,snr_thresh3,snr_thresh4,band_thresh,noise_thresh):
	sm_out=0
	con_out=0
	lines=f.split('\n')
	elts0=lines[0].split(',')
	elts1=lines[1].split(',')
	signal=elts1[53:57]
	noise=elts1[57:61]
	snrs=elts1[61:65]
	noise_result=elts1[79].strip()
	snrs=[math.ceil(float(i)) if i != 'NaN' else 0 for i in snrs ]
	signal=[i if i != 'NaN' else '0' for i in signal ]
	noise=[int(float(i)) if i != 'NaN' else 0 for i in noise ]

	count=0
	# for i in snrs:
	# 	if math.ceil(float(i))>=snr_thresh:
	# 		count+=1
	if math.ceil(float(snrs[0])) >= snr_thresh1:
		count+=1
	if math.ceil(float(snrs[1])) >= snr_thresh2:
		count+=1
	if math.ceil(float(snrs[2])) >= snr_thresh3:
		count+=1
	if math.ceil(float(snrs[3])) >= snr_thresh4:
		count+=1

	result='2'
	result_human='Refer'
	if count>=band_thresh:
		result='1'
		result_human='Pass'

	if con=='1':
		con_out=(0)
	elif con=='2':
		con_out=(1)
	if result=='1':
		sm_out=(0)
	elif result=='2':
		sm_out=(1)

	counter=0
	noise_result2='noise-pass'
	for i in noise:
		if i>=noise_thresh: # old thresh is 98, 93 is a good threshold
			counter+=1

	if counter>=2:
		noise_result2='retry'

	if result!=con and noise_result2=='noise-pass':
		print (">>%s %d %d %d %d | %d %d %d %d %s %s"%(fname,math.ceil(float(snrs[0])),math.ceil(float(snrs[1])),
			math.ceil(float(snrs[2])),math.ceil(float(snrs[3])),
			float(noise[0]),float(noise[1]),float(noise[2]),float(noise[3]),result_human,result_code[con]))
	# if result!=con:
	# 	print ('>>',(fname,np.sum(noise),noise))
	# else:
	# 	print ((fname,np.sum(noise),noise))
	# if noise_result2=='retry':
	# print ('"'+fname[:-12]+'",')
	return sm_out,con_out,result,noise_result,noise_result2,snrs

fout=open('logs.txt','w+')
best_acc=0
best_thresh=[0,0,0,0]
exclude_left=[152]
exclude_right=[152]
for snr_thresh1 in [7]:
	for snr_thresh2 in [7]:
		for snr_thresh3 in [11]:
			for snr_thresh4 in [12]:
				for band_thresh in [2]:
					for noise_thresh in [80]:
					# for noise_thresh in np.arange(70,120,5):
						correct=0
						total_complete=0
						total_all=0
						con_incomplete=0
						sm_incomplete=0
						snr_out=[]
						sm_out=[]
						con_out=[]
						for line in lines[3:-1]:
							elts=line.split(',')
							# print (elts)
							site=site_code[elts[0]]
							pid=elts[1]

							con_right1_done=elts[7]
							con_right1_res=elts[8]
							con_right2_res=elts[9]

							sm_right1_done=elts[10]
							sm_right1_res=elts[11]
							sm_right2_res=elts[12]

							con_left1_done=elts[13]
							con_left1_res=elts[14]
							con_left2_res=elts[15]

							sm_left1_done=elts[16]
							sm_left1_res=elts[17]
							sm_left2_res=elts[18]
							
							attempt_left=1
							attempt_right=1

							if len(con_right2_res)>0:
								con_right=con_right2_res
							else:
								con_right=con_right1_res
							if len(con_left2_res)>0:
								con_left=con_left2_res
							else:
								con_left=con_left1_res
							if len(sm_left2_res)>0:
								sm_left=sm_left2_res
								attempt_left=2
							else:
								sm_left=sm_left1_res
								attempt_left=1
							if len(sm_right2_res)>0:
								sm_right=sm_right2_res
								attempt_right=2
							else:
								sm_right=sm_right1_res
								attempt_right=1
							if pid=='180':
								attempt_right=1

							if len(con_right)>0 and result_code[con_right]!='Incomplete' and \
								len(sm_right)>0 and result_code[sm_right]!='Incomplete' and int(pid) not in exclude_right:
								fname="%s-.*-right-%d"%(pid,attempt_right)
								# print (fname,con_right,sm_right)
								out=find_file(fname)
								if out:
									fsummary=open ('../kenya_files/'+out).read()
									out2=out.replace('summary','checkfit')
									out2=out2.replace('csv','txt')
									checkfit=np.loadtxt ('../kenya_files/'+out2)[-1]
									sm_out_elt,con_out_elt,sm_right,noise_result,noise_result2,snrs=parse_summary(
										out,fsummary,con_right,snr_thresh1,snr_thresh2,snr_thresh3,snr_thresh4,
										band_thresh,noise_thresh)
									if noise_result2=='retry':
										# print (out,'retry')
										continue
									sm_out.append(sm_out_elt)
									con_out.append(con_out_elt)
									snr_out.append(snrs)
									# print ('"'+out[:-12]+'",'+noise_result)
									if con_right==sm_right:
										correct+=1
									# else:
									# 	print ("%-8s %s right CON:[%s %s] SM:[%s %s] %d\n"%(site,pid,result_code[con_right1_res],result_code[con_right2_res],
									# 		result_code[sm_right1_res],result_code[sm_right2_res],checkfit))
									total_complete+=1
								# else:
								# 	print ('err')

							if len(con_left)>0 and result_code[con_left]!='Incomplete' and \
								len(sm_left)>0 and result_code[sm_left]!='Incomplete' and int(pid) not in exclude_left:
								fname="%s-.*-left-%d"%(pid,attempt_left)
								# print (fname)
								out=find_file(fname)
								if out:
									fsummary=open ('../kenya_files/'+out).read()
									out2=out.replace('summary','checkfit')
									out2=out2.replace('csv','txt')
									checkfit=np.loadtxt ('../kenya_files/'+out2)[-1]
									sm_out_elt,con_out_elt,sm_left,noise_result,noise_result2,snrs=parse_summary(
										out,fsummary,con_left,snr_thresh1,snr_thresh2,snr_thresh3,snr_thresh4,
										band_thresh,noise_thresh)
									if noise_result2=='retry':
										# print (out,'retry')
										continue
									# print ('"'+out[:-12]+'",'+noise_result)
									sm_out.append(sm_out_elt)
									con_out.append(con_out_elt)
									snr_out.append(snrs)
									if con_left==sm_left:
										correct+=1
									# else:
									# 	print ("%-8s %s left CON:[%s %s] SM:[%s %s] %d\n"%(site,pid,result_code[con_left1_res],result_code[con_left2_res],
									# 		result_code[sm_left1_res],result_code[sm_left2_res],checkfit))
									total_complete+=1
								# else:
								# 	print ('err')

							# print ('>>',con_left,sm_left,con_right,sm_right)
							# if con_left and sm_left and len(con_left)>0 and len(sm_left)>0:
							# 	total_all+=1
							# if con_right and sm_right and len(con_right)>0 and len(sm_right)>0:
							# 	total_all+=1
							# if result_code[sm_right1_res]=='Incomplete' or result_code[sm_right2_res]=='Incomplete':
							# 	sm_incomplete+=1
							# if result_code[sm_left1_res]=='Incomplete' or result_code[sm_left2_res]=='Incomplete':
							# 	sm_incomplete+=1
							# if result_code[con_right1_res]=='Incomplete' or result_code[con_right2_res]=='Incomplete':
							# 	con_incomplete+=1
							# if result_code[con_left1_res]=='Incomplete' or result_code[con_left2_res]=='Incomplete':
							# 	con_incomplete+=1

						# conf=confusion_matrix(con_out, sm_out)
						tn, fp, fn, tp = confusion_matrix(con_out, sm_out).ravel()
						print (tp,fp,tn,fn)
						sensi=tp/(tp+fn)
						speci=tn/(tn+fp)
						print ("sensi %.3f speci %.3f"%(sensi,speci))

						# print (results)
						print ("%d %d %d %d %d %d Match rate: %d / %d (%.3f)"%(snr_thresh1,snr_thresh2,snr_thresh3,snr_thresh4,band_thresh,noise_thresh,correct,total_complete,correct/total_complete))
						# fout.flush()
						# print ("CON incomplete: %d / %d (%.2f)\nSM incomplete: %d / %d (%.2f)"%(con_incomplete,total_all,con_incomplete/total_all,
							# sm_incomplete,total_all,sm_incomplete/total_all))
						# if correct/total_complete>best_acc:
						if sensi>best_acc:
							best_acc=correct/total_complete
							# best_acc=sensi
							best_thresh=[snr_thresh1,snr_thresh2,snr_thresh3,snr_thresh4]
							best_band=band_thresh
						# plt.figure()
						# plt.hist(list(itertools.chain(*snr_out)))
						# plt.show()

print ('best ',best_acc)
print (best_thresh)
print (best_band)
fout.flush()
fout.close()





























