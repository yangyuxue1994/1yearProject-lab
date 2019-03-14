import pandas as pd
import pprint as p
import numpy as np

PATH="/Users/cheryang/Documents/UW/1YearProject_debug/data_analysis_code/"
FIXED_SF_SEQ = ["S","S","F","S","S","F","S","S","F","S","S","F","S","S","F","S","S","F","S","S","F","S","S","F","S","S","F","S","S","F","S","S","F","S","S","F","S","S","F","S","S","F","S","S","F","S","S","F","S","S","F","S","S","F","S","S","F","S","S","F","S","S","F","S","S","F","S","S","F","S","S","F","S","S","F","S","S","F","S","S","F","S","S","F","S","S","F","S","S","F","S","S","F","S","F","F","F","F","F","F"]; 


def read_data(subjNum):
	col=['rt', 'stimulus', 'phase', 'resp_iscorrect', 'responses']
	path=PATH+"ASP_v1_ori/ASP_v1_"+str(subjNum)+"_data.csv"
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
	comb  = pd.concat([dfv, dfd], axis=1)

	# only access s
	dfs = comb.loc[comb['stimulus'].str.contains('S', regex=True)].reset_index(drop=True)
	return dfs

def read_randorv1(subjNum):
	col=['prime_type', 'prime_image_ID', 'sentence','prime_verb','targ_verb','verif_ans']
	path = PATH+"ASP_v1_new/ASP_v1_"+str(subjNum)+"_randOrder.csv"
	df = pd.read_csv(path, header=0, index_col=False, usecols=col)
	return df

def files (subjNumList):
	for subjNum in subjNumList:
		ddf = read_data(subjNum)
		odf = read_randorv1(subjNum)
		res = pd.concat([ddf, odf], axis=1, ignore_index=True)
		res.columns = np.append(ddf.columns.values, odf.columns.values)
		res.to_csv(PATH+'pre_processing_data/ASP_v1_'+str(subjNum)+"_prepro.csv", index=False)
		print('doen'+str(subjNum))

files(range(130,140))