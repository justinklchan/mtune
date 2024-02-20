lines=open('../MTUNEPractice-ConventionalVSSmartp_DATA_2024-02-19_0518.csv').read().split('\n')

correct=0
total_complete=0
total_all=0
con_incomplete=0
sm_incomplete=0

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

for line in lines[3:-1]:
	elts=line.split(',')
	# print (elts)
	site=site_code[elts[0]]
	pid=elts[1]
	con_right1_done=elts[7]
	sm_right1_done=elts[8]
	con_right1_res=elts[9]
	sm_right1_res=elts[10]
	con_right2_res=elts[11]
	sm_right2_res=elts[12]
	con_left1_done=elts[13]
	sm_left1_done=elts[14]
	con_left1_res=elts[15]
	sm_left1_res=elts[16]
	con_left2_res=elts[17]
	sm_left2_res=elts[18]

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
	else:
		sm_left=sm_left1_res
	if len(sm_right2_res)>0:
		sm_right=sm_right2_res
	else:
		sm_right=sm_right1_res

	if len(con_right)>0 and result_code[con_right]!='Incomplete' and \
		len(sm_right)>0 and result_code[sm_right]!='Incomplete':
		if con_right==sm_right:
			correct+=1
		else:
			print ("%-8s %s right CON:[%s %s] SM:[%s %s]"%(site,pid,result_code[con_right1_res],result_code[con_right2_res],
				result_code[sm_right1_res],result_code[sm_right2_res]))
		total_complete+=1
	if len(con_left)>0 and result_code[con_left]!='Incomplete' and \
		len(sm_left)>0 and result_code[sm_left]!='Incomplete':
		if con_left==sm_left:
			correct+=1
		else:
			print ("%-8s %s left CON:[%s %s] SM:[%s %s]"%(site,pid,result_code[con_left1_res],result_code[con_left2_res],
				result_code[sm_left1_res],result_code[sm_left2_res]))
		total_complete+=1

	if len(con_left)>0 and len(sm_left)>0:
		total_all+=1
	if len(con_right)>0 and len(sm_right)>0:
		total_all+=1
	if result_code[sm_right1_res]=='Incomplete' or result_code[sm_right2_res]=='Incomplete':
		sm_incomplete+=1
	if result_code[sm_left1_res]=='Incomplete' or result_code[sm_left2_res]=='Incomplete':
		sm_incomplete+=1
	if result_code[con_right1_res]=='Incomplete' or result_code[con_right2_res]=='Incomplete':
		con_incomplete+=1
	if result_code[con_left1_res]=='Incomplete' or result_code[con_left2_res]=='Incomplete':
		con_incomplete+=1

print ("Match rate: %d / %d (%.2f)"%(correct,total_complete,correct/total_complete))
print ("CON incomplete: %d / %d (%.2f)\nSM incomplete: %d / %d (%.2f)"%(con_incomplete,total_all,con_incomplete/total_all,
	sm_incomplete,total_all,sm_incomplete/total_all))