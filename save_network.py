
# coding: utf-8

import pandas as pd 
import networkx as nx
import pickle
from os import listdir
from os.path import isfile, join
import sys
import math
import ast
import sys


def clean(x):
    """ Converts string to list
    """
    if type(x) == float:
        return []
    else: 
        return ast.literal_eval(x)

def convert_date(date_lst):
    """ Converts a string type date into a datetime type date
    """
    if date_lst == []:
        return None
    date = date_lst[0].strip(" ")
    try:
        date = datetime.strptime(date, '%Y-%m-%d')
        return date
    except:
#         print(date)
        return None

def get_files(path):
    """ Returns a list of files in a directory
        Input parameter: path to directory
    """
    mypath = path
    complete = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return complete

def load_df(path, file):
    """ Loads a csv file, returns a dataframe
        Input parameters:
        1. path - to directory containing a file
        2. file - name of the file
    """
    return pd.read_csv(path+"/"+file)


# In[40]:

def set_attributes(dataframe, attribute_dataframe, graph_type = 'dir'):
    """ Returns a network with attributes assigned to each node
        Input parameters:
        1. dataframe - edge list
        2. attribute_dataframe - contains node id, and attributes (name, parrty, nationality, occupation, gender)
        3. graph_type - 'dir' or 'undir'
    """
    
    # load dataframe as graph
    if graph_type == 'dir':
        G = nx.from_pandas_dataframe(dataframe,'from','to', edge_attr=False, create_using=nx.DiGraph())
    elif graph_type == 'undir':
        G = nx.from_pandas_dataframe(dataframe,'from','to', edge_attr=False, create_using=nx.Graph())

#     G = nx.from_pandas_dataframe(dataframe,'from','to')
    # get list of nodes
    node_list = G.nodes()
    # create dictionaries
    data = attribute_dataframe[attribute_dataframe["ID"].isin(node_list)]
    name_data = data[["ID","name"]].set_index('ID')['name'].to_dict()
    gender_data = data[["ID","gender"]].set_index('ID')['gender'].to_dict()
    occupation_data = data[["ID","occupation"]].set_index('ID')['occupation'].to_dict()
    nationality_data = data[["ID","nationality"]].set_index('ID')['nationality'].to_dict()
    party_data = data[["ID","party"]].set_index('ID')['party'].to_dict()
    # set attributes 
    nx.set_node_attributes(G, 'gender', gender_data)
    nx.set_node_attributes(G, 'name', name_data)
    nx.set_node_attributes(G, 'occupation', occupation_data)
    nx.set_node_attributes(G, 'nationality', nationality_data)
    nx.set_node_attributes(G, 'party', party_data)
    
    #print stuff
    num_n = len(G.nodes())
    num_e = len(G.edges())
    print("Number of nodes: ", num_n)
    print("Number of edges: ", num_e)
    
    return G, num_n, num_e 

def save_network(G, path_save,file,graph_type):
    """ Saves network on specified path as PICKLE
        Input parameters:
        1. Graph
        2. path_save - path to directory
        3. file name
        4. graph_type, if dir graph sufix added to title
    """
    if graph_type == "dir":
        print("Network saved as pickle on PATH: ", path_save+"/"+file+"_"+graph_type)
        nx.write_gpickle(G,path_save+"/"+file+"_"+graph_type)
    else:
        print("Network saved as pickle on PATH: ", path_save+"/"+file)
        nx.write_gpickle(G,path_save+"/"+file)



if __name__ == "__main__":

    path_files = sys.argv[1]
    path_save = sys.argv[2]
    graph_type = sys.argv[3]

    # clean politician data
    politician_data = pd.read_csv("data/politician-data.csv",quotechar='"',sep="\t",converters=
                              {"occupation":ast.literal_eval})

    politician_data["party"] = politician_data["party"].apply(clean)


    politician_data["nationality"] = politician_data["nationality"].apply(clean)

    politician_data["name"] = politician_data["name"].apply(clean)

    politician_data["birthDate"] = politician_data["birthDate"].apply(clean)
    politician_data["deathDate"] = politician_data["deathDate"].apply(clean)

    politician_data["birthDate"] = politician_data["birthDate"].apply(convert_date)
    politician_data["deathDate"] = politician_data["deathDate"].apply(convert_date)

    
    files = get_files(path_files)



    lst = []
    for file in files:
        print(file)
        net_df = load_df(path_files,file)
        G, num_n, num_e = set_attributes(net_df, politician_data,graph_type)
        sub_lst = [file,num_n, num_e]
        lst.append(sub_lst)
        save_network(G,path_save,file.replace(".csv",""),graph_type)         
    df = pd.DataFrame(lst)
    df.columns = ["file","nodes","edges"]
    if graph_type == 'dir':
        df.to_csv(path_save+"/stats_{}.csv".format(graph_type))
    else:
        df.to_csv(path_save+"/stats.csv")



