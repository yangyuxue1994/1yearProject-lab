#!/usr/bin/python

import sys
import randor 
import organize
import v4_processeach as v4

## GLOBAL PARAM
SUBJ_LIST = [];

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
    SUBJ_LIST = range(start_subj_num, end_subj_num+1)
    print ('SUBJ_LIST: ',SUBJ_LIST)

    # do transpose
    randor.reformat_files(SUBJ_LIST)
    print('finish randor')

    # run organize
    organize.generate_preprop_files(SUBJ_LIST)
    print ('finish generate_preprop_files')

    # run post_processing
    v4.SUBJ_LIST = SUBJ_LIST
    v4result = v4.all_mean_activeratio_primetype()

if __name__ == "__main__":
    main()

    ###
    # go to dir
    # > python -m prep 1000 1001 'v4'