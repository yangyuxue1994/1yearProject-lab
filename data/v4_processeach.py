import pandas as pd
import numpy as np
import sys
# from nltk import word_tokenize, pos_tag
# import postagger
import os
import passive

## GLOBAL PARAM
PRE_DIR = './pre_processing_data/'
POST_DIR= './post_processing_data/'
SUBJ_LIST = []
VER = 'v4'
ONLY_CORRECT = True

def load_prepropdata (subjNum):	
	cols=['P_type', 'T_verb','P_sentence','resp_iscorrect', 'verif_rt', 'descr_rt', 'responses','verif_ans']
	df = pd.read_csv(PRE_DIR+'ASP_'+ VER +'_'+str(subjNum)+'_prepro.csv', usecols=cols)
	return df

# this function return an overall numeric value of accuracy in verif task
def get_subj_verif_accuracy(currdf):
	return float(sum(currdf.resp_iscorrect))/float(len(currdf.index))

#  this function return df of accuracy on 4 prime type 
def get_subj_verif_accuracy_primetype(currdf):
	df_totalcount = currdf.groupby('P_type').count()[['resp_iscorrect']]
	df_correctcount = currdf.groupby('P_type').sum()[['resp_iscorrect']]
	df_accuracy = df_correctcount.div(df_totalcount, axis=1)
	return df_accuracy

# this function calculates mean of verif rt based on 4 prime type
def get_subj_verifRT_pimetype(currdf):
	return currdf.groupby('P_type').mean()[['verif_rt']]

def clean_currdf(subjNum):
	# currdf = null;
	export_post_f=POST_DIR+'ASP_'+ VER +'_'+str(subjNum)+'_postpro.csv'
	# if exists, import 
	if (os.path.exists(export_post_f)):
		print ('already exists, importing...')
		currdf = pd.read_csv(export_post_f)
	else:
		print('exporting... ')
		currdf = load_prepropdata(subjNum)
		### re-format: {"Q0":"Man pulls the slave"} remove characters 
		resp_list = currdf.responses.values.tolist()	
		clear_resp_list = [s.replace('{','').replace('"','').replace('}','').split(':')[1] for s in resp_list]
		tense_list = [passive.decide_if_active(s) for s in clear_resp_list]
		
		#cl_resp_df = pd.DataFrame({'clear_responses':clear_resp_list})
		# add new column to currdf
		currdf['clear_responses'] = pd.Series(clear_resp_list, dtype=str)
		currdf['isactive'] = pd.Series(tense_list)
		currdf.to_csv(export_post_f, index=False)

	# check empty responses
	currdf = currdf.dropna(axis=0, how='any')

	# select only correct trials
	if (ONLY_CORRECT != None):
		currdf = currdf.loc[currdf['resp_iscorrect'] == ONLY_CORRECT]

	return currdf


# this function return df of active-tense proportion on 4 prime type
def get_subj_activeratio_primetype(currdf):
	df_totalcount = currdf.groupby('P_type').count()[['isactive']]
	df_activecount = currdf.groupby('P_type').sum()[['isactive']]
	df_active_ratio = df_activecount.div(df_totalcount, axis=1)
	return df_active_ratio

# # resp_allcorrect: True/Flase
# def get_subj_correct_activeratio_primetype_allcorrect(currdf, resp_allcorrect):
# 	# get only correct/incorrect trials and count active/passive
# 	corrdf = currdf.loc[currdf['resp_iscorrect'] == resp_allcorrect]
# 	df_totalcount = corrdf.groupby('P_type').count()[['isactive']]
# 	df_activecount = corrdf.groupby('P_type').sum()[['isactive']]
# 	df_active_ratio = df_activecount.div(df_totalcount, axis=1)
# 	return df_active_ratio


# semantically correct trials are verif_ans always y
def get_subj_activeratio_primetype_semcorrect(currdf, verif_ans):
	sem_df = currdf.loc[currdf['verif_ans'] == verif_ans]
	return get_subj_activeratio_primetype(sem_df)


######### subject list #########
def all_mean_verif_accuracy():
	all_acc = [get_subj_verif_accuracy(clean_currdf(subjNum)) for subjNum in SUBJ_LIST]
	return np.mean(all_acc)

##todo not correct
def all_mean_verif_accuracy_primetype():
	all_acc_primetype = [get_subj_verif_accuracy_primetype(clean_currdf(subjNum)) for subjNum in SUBJ_LIST]
	dfconc = pd.concat(all_acc_primetype)
	dfallmean = dfconc.groupby('P_type').mean()
	return dfallmean

def all_mean_verifRT_pimetype():
	all_verifRT_pimetype = [get_subj_verifRT_pimetype(clean_currdf(subjNum)) for subjNum in SUBJ_LIST]
	dfconc = pd.concat(all_verifRT_pimetype)
	dfallmean = dfconc.groupby('P_type').mean()
	return dfallmean

def all_mean_activeratio_primetype():
	all_activeratio_primetype = [get_subj_activeratio_primetype(clean_currdf(subjNum)) for subjNum in SUBJ_LIST]
	dfconc = pd.concat(all_activeratio_primetype)
	dfallmean = dfconc.groupby('P_type').mean()
	return dfallmean

# this function is similar to all_mean_activeratio_primetype() but only count based on 
# semantically correct/incorrect trials
# very_asn = y/n
def all_mean_activeratio_primetype_semantic(semantic_correct):
	# only get thoes semantically correct trials
	all_activeratio_primetype = [get_subj_activeratio_primetype_semcorrect(clean_currdf(subjNum), semantic_correct) for subjNum in SUBJ_LIST]
	dfconc = pd.concat(all_activeratio_primetype)
	dfallmean = dfconc.groupby('P_type').mean()
	return dfallmean




######### RUN INSTRUCTION #########
### in terminal >> edm shell --environment psiturk
### go to main dir
# > python 
# > import v4_processeach as v

### example for 'v4'
# > v.VER = 'v4'
# > v.ONLY_CORRECT = True/None
# > v.SUBJ_LIST = []
# > v.SUBJ_LIST = range(1000,1002)
# > v4result = v.all_mean_activeratio_primetype()
# [1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010, 1011, 1013, 1014, 1015, 1016, 1017, 1018, 1019, 1020, 1021, 1023, 1024, 1025, 1026, 1027]

'''
def main():
	argument_list = ['start: ', 'end: ', 'version: ']

    start_subj_num = int(sys.argv[1])
    end_subj_num = int(sys.argv[2])
    version = sys.argv[3]

    # print command line arguments
    for i in range(len(sys.argv[1:])):
        arg = sys.argv[1:][i]
        print (argument_list[i],arg)

    # update global param
    SUBJ_LIST = range(start_subj_num, end_subj_num)

if __name__ == "__main__":
    main()
'''
