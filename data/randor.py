import pandas as pd
import ast
import os

PATH="./"
VER = 'v5'

def change_rand_file_format(f):
	df=pd.read_csv(f)
	df=df.T
	# df=df.iloc[6:]
	
	if (VER == 'v5'):
		df=df.iloc[:-6]
	if (VER == 'v4'):
		df=df.iloc[:-6] 

	newdf = pd.DataFrame()
	for index, row in df.iterrows():
		strrow=row.loc[0]
		dicrow=ast.literal_eval(strrow)
		dfrow=pd.DataFrame.from_dict(dicrow, orient="index").T
		newdf=newdf.append(dfrow, ignore_index=True)
	return newdf


def reformat_files(subjNum_list):
	for subjNum in subjNum_list:
		old_file_name=PATH+"ASP_"+VER+"_ori/ASP_"+VER+"_"+str(subjNum)+"_randOrder.csv"
		new_file_name=PATH+"ASP_"+VER+"_new/ASP_"+VER+"_"+str(subjNum)+"_randOrder.csv"
		newdf=change_rand_file_format(old_file_name)
		# seqdf = pd.DataFrame({"seq":FIXED_SF_SEQ})
		# newdf.loc[:,'seq']=seqdf['seq']
		
		# check file exits
		if (os.path.exists(new_file_name)):
			print('already have pre-processing data!')
		else:
			newdf.to_csv(new_file_name)
			print ('finish transpose!' + str(subjNum))

# reformat_files(range(143,146))

