
# coding: utf-8

# In[33]:

import pandas as pd 
import sys
import filter_edgelist_data as fltr 
import stats
import save_network as sn
import networkx as nx


path_copy = sys.argv[1]
path_paste = sys.argv[2]
filter_file = sys.argv[3]


files_df = pd.read_csv(filter_file)
files = files_df['file_name'].values
fltr.copy_files(files, path_copy, path_paste+"/all")

c_names = {
    'us':"american",
    "de": "german",
    "gb": "british",
    "fr": "french",
    "ru": "russian"
}

for name in c_names.keys():
    for file in files: 
        G = nx.read_gpickle(path_copy+file)
        fG = stats.filter_graph(G, "nationality", c_names[name])
        save = path_paste+name
        sn.save_network(fG, save, file, 'dir')