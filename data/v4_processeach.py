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

def load_prepropdata (subjNum):	
	cols=['P_type', 'T_verb','P_sentence','resp_iscorrect', 'verif_rt', 'descr_rt', 'responses','verif_ans']
	df = pd.read_csv(PRE_DIR+'ASP_'+ VER +'_'+str(subjNum)+'_prepro.csv', usecols=cols)
	#dflist = [pd.read_csv(DIR+'ASP_v2_'+str(subjNum)+'_prepro.csv', usecols=cols) for subjNum in SUBJ_LIST]
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
	currdf = load_prepropdata(subjNum)
	### re-format: {"Q0":"Man pulls the slave"} remove characters 
	resp_list = currdf.responses.values.tolist()	
	clear_resp_list = [s.replace('{','').replace('"','').replace('}','').split(':')[1] for s in resp_list]
	tense_list = [passive.decide_if_active(s) for s in clear_resp_list]
	
	#cl_resp_df = pd.DataFrame({'clear_responses':clear_resp_list})
	# add new column to currdf
	currdf['clear_responses'] = pd.Series(clear_resp_list, dtype=str)
	currdf['isactive'] = pd.Series(tense_list)

	##to csv
	export_post_f=POST_DIR+'ASP_'+ VER +'_'+str(subjNum)+'_postpro.csv'
	if (os.path.exists(export_post_f)):
		print ('already exported')
	else:
		currdf.to_csv(export_post_f, index=False)
		print('exporting post-process data')
	return currdf


# this function return df of active-tense proportion on 4 prime type
def get_subj_activeratio_primetype(currdf):
	df_totalcount = currdf.groupby('P_type').count()[['isactive']]
	df_activecount = currdf.groupby('P_type').sum()[['isactive']]
	df_active_ratio = df_activecount.div(df_totalcount, axis=1)
	return df_active_ratio

######### subject list #########
def all_mean_verif_accuracy():
	all_acc = [get_subj_verif_accuracy(load_prepropdata(subjNum)) for subjNum in SUBJ_LIST]
	return np.mean(all_acc)

##todo not correct
def all_mean_verif_accuracy_primetype():
	all_acc_primetype = [get_subj_verif_accuracy_primetype(load_prepropdata(subjNum)) for subjNum in SUBJ_LIST]
	dfconc = pd.concat(all_acc_primetype)
	dfallmean = dfconc.groupby('P_type').mean()
	return dfallmean

def all_mean_verifRT_pimetype():
	all_verifRT_pimetype = [get_subj_verifRT_pimetype(load_prepropdata(subjNum)) for subjNum in SUBJ_LIST]
	dfconc = pd.concat(all_verifRT_pimetype)
	dfallmean = dfconc.groupby('P_type').mean()
	return dfallmean



def all_mean_activeratio_primetype():
	all_activeratio_primetype = [get_subj_activeratio_primetype(clean_currdf(subjNum)) for subjNum in SUBJ_LIST]
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
# > v.SUBJ_LIST = []
# > v.SUBJ_LIST = range(1000,1002)
# > v4result = v.all_mean_activeratio_primetype()


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
