# 1yearProject-lab

## Data Analysis:

### Folders
	Data/ASP_v2_ori: raw data and randomized sequence file
		ASP_v2_143_data.csv
		ASP_v2_143_randOrder.csv

	Data/ASP_v2_new: after re-formating randomization csv file 

	Data/pre_processing_data: real trial order while subjects do tasks
		'v1' : 63 trials (remove fillers) ASP_v1_130_prepro.csv
		'v2': 100 trials (including fillers) ASP_v2_143_prepro.csv

### Deal with Data
	required packages:
		- pandas
		- nltk
		- numpy

	1. Pre-processing data
	in main folder, run 
		```bash-3.2$ python run_pre.py start_subject_num, end_subject_num,'version'```
		```python run_pre.py 215 216 'v2'```
  
  After running pre-processing script, raw data and randomization file will be combined and exported into *pre_processing_data* folder

	2. Analyzing data
	In main folder, start python

	```import v2_processeach as v```

	### set SUBJ_LIST
	```
	v.SUBJ_LIST = [num1, num2]
	v.VER = 'v2'
	```

	### examples for 'v1'
	```
	v.VER = 'v1'
	v.SUBJ_LIST = range(130,140)
	v1result = v.all_mean_activeratio_primetype()
  ```

	### example for 'v2'
	```
	v.VER = 'v2'
	v.SUBJ_LIST = range(143,151)
	v.SUBJ_LIST.extend( range(210,216) )
	v2result = v.all_mean_activeratio_primetype()
	```







		
		
