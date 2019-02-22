import pandas as pd
import pprint as p
import numpy as np
import os

PATH="./"
FIXED_SF_SEQ = ["S","S","F","S","S","F","S","S","F","S","S","F","S","S","F","S","S","F","S","S","F","S","S","F","S","S","F","S","S","F","S","S","F","S","S","F","S","S","F","S","S","F","S","S","F","S","S","F","S","S","F","S","S","F","S","S","F","S","S","F","S","S","F","S","S","F","S","S","F","S","S","F","S","S","F","S","S","F","S","S","F","S","S","F","S","S","F","S","S","F","S","S","F","S","F","F","F","F","F","F"]; 


def read_data(subjNum):
	col=['rt', 'stimulus', 'phase', 'resp_iscorrect', 'responses']
	path=PATH+"ASP_v2_ori/ASP_v2_"+str(subjNum)+"_data.csv"
	df = pd.read_csv(path, header=0, usecols=col, index_col=False)
	df = df.loc[df['phase'] == 1] # only access real trial data
	#data_df = df.loc[df['stimulus'] is 'S'] # only select S responses

	df['verif_rt'] = np.nan
	df['descr_rt'] = np.nan
	df['verif_rt'].update(df.loc[pd.isnull(df.responses)]['rt'])
	df['descr_rt'].update(df.loc[~pd.isnull(df.responses)]['rt'])

	# detach columns
	dfv = df.drop(['responses', 'descr_rt'], axis=1).dropna(axis=0, how='any').reset_index(drop=True)
	dfd = df[['responses', 'descr_rt']].dropna(axis=0, how='all').reset_index(drop=True).dropna(axis=0, how='any').reset_index(drop=True)

	# comb c
	comb  = pd.concat([dfv, dfd], axis=1, sort=False).reset_index(drop=True)

	# only access s
	# dfs = comb.loc[comb['stimulus'].str.contains('S', regex=True)].reset_index(drop=True)
	return comb

def read_randorv2(subjNum):
	col=['prime_type', 'prime_image_ID', 'sentence','prime_verb','targ_verb','verif_ans']
	path = PATH+"ASP_v2_new/ASP_v2_"+str(subjNum)+"_randOrder.csv"
	df = pd.read_csv(path, header=0, index_col=False, usecols=col)
	return df

def generate_preprop_files (subjNumList):
	for subjNum in subjNumList:
		ddf = read_data(subjNum)
		odf = read_randorv2(subjNum)
		res = pd.concat([ddf, odf], axis=1, ignore_index=True, sort=False)
		res.columns = np.append(ddf.columns.values, odf.columns.values)
		dest_file_path = PATH+'pre_processing_data/ASP_v2_'+str(subjNum)+"_prepro.csv"
		## check exists
		if (os.path.exists(dest_file_path)):
			print('already have pre-processing data!')
		else:
			res.to_csv(dest_file_path, index=False)
			print('finish: '+str(subjNum))
	return 
# files(range(130,140))