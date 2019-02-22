#!/usr/bin/python

import sys
import randor 
import v2_prep as v2

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

    # run pre_processing
    v2.generate_preprop_files(SUBJ_LIST)
    print ('finish generate_preprop_files')

if __name__ == "__main__":
    main()

    ###
    # go to dir
    # > python -m RUN_PRE 210 216 'v2'