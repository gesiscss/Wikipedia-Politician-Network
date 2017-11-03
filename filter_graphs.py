
# coding: utf-8

# In[33]:

import pandas as pd 
import sys
import filter_edgelist_data as fltr 



path_copy = sys.argv[1]
path_paste = sys.argv[2]
filter_file = sys.argv[3]


files_df = pd.read_csv(filter_file)
files = files_df['file_name'].values
fltr.copy_files(files, path_copy, path_paste)