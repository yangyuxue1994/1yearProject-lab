import pandas as pd
import numpy as np
import sys
# from nltk import word_tokenize, pos_tag
# import postagger
import os
import passive

## GLOBAL PARAM
DIR = './'
SUBJ_LIST = []
VER = ''

def load_prepropdata (subjNum):
	cols=['prime_type', 'prime_verb','targ_verb','sentence','resp_iscorrect', 'verif_rt', 'descr_rt', 'responses']
	df = pd.read_csv(DIR+'ASP_'+ VER +'_'+str(subjNum)+'_prepro.csv', usecols=cols)
	#dflist = [pd.read_csv(DIR+'ASP_v2_'+str(subjNum)+'_prepro.csv', usecols=cols) for subjNum in SUBJ_LIST]
	return df

# this function return an overall numeric value of accuracy in verif task
def get_subj_verif_accuracy(currdf):
	return float(sum(currdf.resp_iscorrect))/float(len(currdf.index))

#  this function return df of accuracy on 4 prime type 
def get_subj_verif_accuracy_primetype(currdf):
	df_totalcount = currdf.groupby('prime_type').count()[['resp_iscorrect']]
	df_correctcount = currdf.groupby('prime_type').sum()[['resp_iscorrect']]
	df_accuracy = df_correctcount.div(df_totalcount, axis=1)
	return df_accuracy

# this function calculates mean of verif rt based on 4 prime type
def get_subj_verifRT_pimetype(currdf):
	return currdf.groupby('prime_type').mean()[['verif_rt']]

'''
# this function is to determine grammatical structure of this sentence
def determine_tense_input(sentence):
    text = word_tokenize(sentence)
    tagged = pos_tag(text)

    tense = {}
    tense["future"] = len([word for word in tagged if word[1] == "MD"])
    tense["present"] = len([word for word in tagged if word[1] in ["VBP", "VBZ","VBG"]])
    tense["past"] = len([word for word in tagged if word[1] in ["VBD", "VBN", "IN"]]) 
    # return(tense)

    ### if is past tense: return -1; if is active tense: return 1
    result = np.nan
    if (tense['past'] != 0 & ([word[0] for word in tagged if word[1] in ["IN"]][0]=='by')):
    	result = 0
    else:
    	# if (tense['present'] != 0):
    	# 	result = 1
    	result = 1
    return result
'''
# this function return df of active-tense proportion on 4 prime type
def get_subj_activeratio_primetype(currdf):
	### re-format: {"Q0":"Man pulls the slave"} remove characters 
	resp_list = currdf.responses.values.tolist()	
	clear_resp_list = [s.replace('{','').replace('"','').replace('}','').split(':')[1] for s in resp_list]
	tense_list = [passive.decide_if_active(s) for s in clear_resp_list]
	
	#cl_resp_df = pd.DataFrame({'clear_responses':clear_resp_list})
	# add new column to currdf
	currdf['clear_responses'] = pd.Series(clear_resp_list, dtype=str)
	currdf['tense'] = pd.Series(tense_list)

	df_totalcount = currdf.groupby('prime_type').count()[['tense']]
	df_activecount = currdf.groupby('prime_type').sum()[['tense']]
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
	dfallmean = dfconc.groupby('prime_type').mean()
	return dfallmean

def all_mean_verifRT_pimetype():
	all_verifRT_pimetype = [get_subj_verifRT_pimetype(load_prepropdata(subjNum)) for subjNum in SUBJ_LIST]
	dfconc = pd.concat(all_verifRT_pimetype)
	dfallmean = dfconc.groupby('prime_type').mean()
	return dfallmean



def all_mean_activeratio_primetype():
	all_activeratio_primetype = [get_subj_activeratio_primetype(load_prepropdata(subjNum)) for subjNum in SUBJ_LIST]
	dfconc = pd.concat(all_activeratio_primetype)
	dfallmean = dfconc.groupby('prime_type').mean()
	return dfallmean



######### RUN INSTRUCTION #########
### in terminal >> edm shell --environment psiturk
### go to main dir
# > python 
# > import v2_processeach as v

### set SUBJ_LIST
# > v.SUBJ_LIST = [num1, num2]
# > v.VER = 'v2'

### can use functions to calculate

### examples for 'v1'
# > v.VER = 'v1'
# > v.SUBJ_LIST = range(130,140)
# > v1result = v.all_mean_activeratio_primetype()

### example for 'v2'
# > v.VER = 'v2'
# > v.SUBJ_LIST = []
# > v.SUBJ_LIST = range(143,151)
# > v.SUBJ_LIST.extend( range(210,216) )
# > v2result = v.all_mean_activeratio_primetype()

### comb v1 res and v2 res


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
