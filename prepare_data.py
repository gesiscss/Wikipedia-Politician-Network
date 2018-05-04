
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
from datetime import datetime
from matplotlib import pyplot as plt
from itertools import groupby
from collections import Counter
import seaborn as sns
import sys
# get_ipython().magic('matplotlib inline')


# Global lists 
# 
# Complete dataset
#
remove_from_model = []
# Model dataset
#
#
remove_from_all = [""]


def drop_columns(df, lst):
    """ Removes dataframe columns specified in lst
    """
    df = df.drop(lst, axis=1)
    return df 


def get_age(x, thres=110):
    """ Calculates age of politicians, if birth unknown age is by default=0
    """
    birth = x["birthDate"]
    death = x["deathDate"]
    
    if birth == None and death == None:
        return 0
    if birth != None and death == None:
        delta = datetime.now() - birth
        age = int(delta.days/365)
        if age < 18:
            return 0
        if age < thres:
            return age
        else:
            return 0
    if birth != None and death != None:
        # it might happen that death is before birth.. 
        delta = death - birth
        if death < birth:
            return -1
        else: 
            age = abs(int(delta.days/365))    
            if age < thres and age >= 18:
                return int(delta.days/365)
            else:
                return 0
    if birth == None and death != None:
        return 0 

def is_alive(x, thres=110):
    """ Returns yes / no / unknown depending on if the politician is alive/dead
    """
    birth = x["birthDate"]
    death = x["deathDate"]
    age = x["age"]
    
    if birth != None and death != None:
        if age != -1:
            return "no"
        else:
            return "unknown"        
    if birth == None and death != None:
        return "no"
    if birth != None and death == None:
        if age > 0:
            return "yes"
        elif age == 0 and int((datetime.now() - birth).days/365) < thres:
            return "unknown"
        elif age == 0 and int((datetime.now() - birth).days/365) >= thres:
            return "no"
    if birth == None and death == None:
        return "unknown"

def add_age(df):
    """ Adds age column to dataframe
    """
    df["age"] = df.apply(lambda x: get_age(x), axis=1)
    return df

def add_alive_status(df):
    df["is_alive"] = df.apply(lambda x: is_alive(x), axis=1)
    return df

def age_distance(date):
    """ Calculates distance from given date to present, if the distance is negative
    it results as a default value -1 
    """
#     print(date)
    if date == None:
        return -1
    else:
        delta = datetime.now() - date
        distance = int(delta.days/365)
        if distance > 0:
            return int(delta.days/365)
        else:
            return -1

def add_distance(df):
    """ Adds 2 columns ["distance_birth"] and ["distance_death"] 
    """
#     if birth_death == "birth":
    df["distance_birth"] = df.apply(lambda x: age_distance(x["birthDate"]),axis=1)
#     elif birth_death == "death":
    df["distance_death"] = df.apply(lambda x: age_distance(x["deathDate"]),axis=1)
    return df

def delta_birth_death(x):
    birth = x["distance_birth"]
    death = x["distance_death"]
    return birth - death

def add_delta(df):
    df["distance_delta"] = df.apply(lambda x: delta_birth_death(x), axis=1)
    return df

def add_lst_size(df,col):
    df[col+"_num"] = df[col].apply(lambda x: len(x))
    return df 

def get_bar_categorical(column_name, title="Politician nationality values distribution", dir_save="../plots/variables"):
    SMALL_SIZE = 26
    MEDIUM_SIZE = 30
    BIGGER_SIZE = 40

    plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
    plt.rc('axes', titlesize=BIGGER_SIZE)     # fontsize of the axes title
    plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
    plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
#     plt.rc('figure', titlesize=BIGGER_SIZE)
#     plt.rc("title", titlesize = BIGGER_SIZE)
    num = sorted([len(i) for i in df[column_name].values.flatten()])
    num = [len(list(group)) for key, group in groupby(num)]
    print(num)
    label = range(0, len(num))
    plt.figure(figsize=(15,10))
    plt.bar(label, num)
    plt.xlabel("Number of {} values".format(column_name))
    plt.xticks(np.arange(min(label), max(label)+1, 1.0))
    plt.ylabel("Frequency")
    plt.title(title)
    path_save = dir_save+"/"+column_name+".jpg"
    plt.savefig(path_save)
    plt.show()

def get_unique_values_multilevel_categorical(df, column_name):
    flat = [i for i in df[column_name].values if len(i)>0]
    flat = sum(flat, [])
    keys = Counter(flat).keys()
    return keys, len(keys)

def get_most_frequent(df, column_name, n):
    flat = [i for i in df[column_name].values if len(i)>0]
    flat = sum(flat, [])
    c = Counter(flat)
    if column_name == "occupation":
        return c.most_common(n+1)[1:]
    return pd.DataFrame(c.most_common(n))

def get_counts(df, column_name, reverse=True):
    flat = [i for i in df[column_name].values if len(i)>0]
    flat = sum(flat, [])
    return sorted(Counter(flat).values(), reverse=reverse)

def get_percentiles(df, col, percentile = [.95]):
    counts = get_counts(df, col, reverse=False)
    c = pd.DataFrame(counts)
#     print(c)
    c.columns = ["count"]
    if col == "occupation":
        c = c[c["count"] != c["count"].max()]
#     c["cumulative"] = c.cumsum()
    return c["count"].describe(percentiles = percentile)

def plot_correlation_map( df , annot=True):
    corr = df.corr()
    _ , ax = plt.subplots( figsize =( 12 , 10 ) )
    cmap = sns.diverging_palette( 220 , 10 , as_cmap = True )
    _ = sns.heatmap(
        corr, 
        cmap = cmap,
        square=True, 
        cbar_kws={ 'shrink' : .9 }, 
        ax=ax, 
        annot = annot, 
        annot_kws = { 'fontsize' : 12 }
    )


def get_from_lst(lst,value):
    """ Returns value if in list, returns "none" if not
    """
#     print(lst)
    lst = [x.strip(" ") for x in lst]
    if value in lst:
#         print(value)
        return value
    else:
        return "none"

def filter_by_value(df, column, value):
    """ Returns dataframe after filtering colums per value 
    """
    df["filter_cols"] = df[column].apply(lambda x: get_from_lst(x, value))
    df = df[df["filter_cols"] == value]
    df = df.drop("filter_cols", axis=1)
    return df

def clean_lst(lst):
    return [x.strip(" ") for x in lst]


def to_binary(lst,value):
#     lst = [x.strip(" ") for x in lst]
    if value in lst:
        return 1
    else:
        return 0
def other_to_bin(x, lst):
    sumed = 0
    for i in lst:
        sumed = sumed + x[i]
    if sumed > 0:
        return 0
    else:
        return 1 
    
def add_binary_column(df, column, column_new, value):
    """ Adds 1 or 0 to a new column, therefore biarising the  
    """
    df[column_new] = df[column].apply(lambda x: to_binary(x, value))

    return df

def get_from_lst(lst,value):
    """ Returns value if in list, returns "none" if not
    """
#     print(lst)
    lst = [x.strip(" ") for x in lst]
    if value in lst:
#         print(value)
        return value
    else:
        return "none"
    
def filter_by_value(df, column, value):
    """ Returns dataframe after filtering colums per value 
    """
    df["filter_cols"] = df[column].apply(lambda x: get_from_lst(x, value))
    df = df[df["filter_cols"] == value]
    df = df.drop("filter_cols", axis=1)
    return df

# numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']

# num_df = df.select_dtypes(include=numerics)
# num_df.columns


# df = drop_columns(df, ['#DBpURL', 'ID', 'WikiURL', 'birthDate', 'deathDate',"name_u"])

def main():
    global remove_from_model
    global remove_from_all



    # Load the data
    df = pd.read_pickle("data/connected_sources/2016")

    # print("cevap")
    # print(model_colums)
    df["party"] = df["party"].apply(lambda x: clean_lst(x))
    df = add_age(df)
    df = add_alive_status(df)
    df = add_distance(df)
    df = add_delta(df)
    df = add_lst_size(df,"nationality")
    df = add_lst_size(df,"party")
    df = add_lst_size(df,"occupation")

    # Dummyfy nationality column
    df = add_binary_column(df,"nationality", "us", "american").head()
    df = add_binary_column(df,"nationality", "de", "german").head()
    df = add_binary_column(df,"nationality", "fr", "french").head()
    df = add_binary_column(df,"nationality", "in", "indian").head()
    df = add_binary_column(df,"nationality", "cd", "canadian").head()
    df = add_binary_column(df,"nationality", "no", "norwegian").head()
    df = add_binary_column(df,"nationality", "ru", "russian").head()
    df = add_binary_column(df,"nationality", "gb", "british").head()
    df["other_n"] = df.apply(lambda x: other_to_bin(x, ["us","de","fr","in","cd","no","ru","gb"]), axis=1)

    # Dummyfy party column
    df = add_binary_column(df,"party", "dem", "democratic party (united states)").head()
    df = add_binary_column(df,"party", "rep", "republican party (united states").head()
    df = add_binary_column(df,"party", "indi", "independent politician").head()
    df = add_binary_column(df,"party", "inc", "indian national congress").head()
    df = add_binary_column(df,"party", "cpc", "communist party of china").head()
    df = add_binary_column(df,"party", "bjp", "bharatiya janata party").head()
    df["other_p"] = df.apply(lambda x: other_to_bin(x, ["dem","rep","indi","inc","cpc","bjp"]), axis=1)

     # Dummyfy occupation column
    df = add_binary_column(df,"occupation", "wrt", "writer").head()
    df = add_binary_column(df,"occupation", "sci", "scientist").head()
    df = add_binary_column(df,"occupation", "jor", "journalist").head()
    df = add_binary_column(df,"occupation", "eco", "economist").head()
    df = add_binary_column(df,"occupation", "hst", "historian").head()
    df = add_binary_column(df,"occupation", "spo", "sportsperson").head()
    df = add_binary_column(df,"occupation", "lyr", "lawyer").head()
    df = add_binary_column(df,"occupation", "phs", "physician").head()
    df = add_binary_column(df,"occupation", "act", "actor").head()
    df = add_binary_column(df,"occupation", "ply", "player").head()
    df["other_o"] = df.apply(lambda x: other_to_bin(x, ["dem","rep","indi","inc","cpc","bjp"]), axis=1)

    df['year_interval'] = pd.cut( df['entered'], [2000,2005,2010,2016], labels=[1,2,3])

    print(df.columns)

    #todo: 
    # save dataset for future use 
    # save model datasets 
    # save numerical? 

if __name__ == '__main__':
    main()


