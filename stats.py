
# coding: utf-8

import pandas as pd 
import networkx as nx
import pickle
from os import listdir
from os.path import isfile, join
import sys
import math


def get_files(path):
    """ Returns a list of files in a directory
        Input parameter: path to directory
    """
    mypath = path
    complete = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return complete

def avg_degree(G):
    """ Returns average degree of the graph and the number of nodes
        Input parameter: G - graph
    """
    degree_values = list(G.degree().values())
    degree_sum = sum(degree_values)
    node_num = len(degree_values)
    avg_degree = degree_sum/node_num
    return avg_degree, node_num

def network_size(G):
    """ Returns number of nodes for a given graph
    """
    degree_values = list(G.degree().values())
    node_num = len(degree_values)
    return node_num


def filter_gender(G,gender):
    """ Returns a filtered subgraph containing nodes with specified gender
        Input parameters:
        1. G - graph
        2. gender - 'male' or 'female'
    """
    return G.subgraph( [n for n,attrdict in G.node.items() if attrdict['gender'] == gender] )


def filter_graph(G, attribute, value):
    """ Returns a filtered subgraph containing nodes with specified attribute
        Input parameters:
        1. G - graph
        2. attribute - filter by this attribute: {gender, occupation, party, nationality}
        3. value - filter by this value, for example 'female' in the case of gender 
    """
    if attribute == "gender":
        return G.subgraph( [n for n,attrdict in G.node.items() if attrdict['gender'] == value] )
    else:
        return G.subgraph( [n for n,attrdict in G.node.items() if value in attrdict[attribute]] )


# files_path = "data/graphs"

# files = get_files(files_path)[:-1]

def get_ratio(x, typ='fm'):
    """ Returns a single value for female to male ratio
        'fm' is for female to male ratio
        'mf' is for male to female ratio
    """
    # print(type(x['f_nodes']))
    # print(type(x['m_nodes']))
    # print(x)
    f = x['f_nodes']
    m = x['m_nodes']
    
    # print(m)
    # print(f.add(1))
    # print(m.add(1))

    if typ == 'fm':
        # if f == 0:
        #     f = float('Inf')
        # if f != 0 and m == 0:
        #     f = f+1
        #     m = m+1
        #     return f/(f+m)
        if f+m ==0:
            return 0
        return f/(f+m)
    if typ == 'mf': 
        if f+m ==0:
             return 0
        return m/(f+m)


def get_ratio_array(df, typ='fm'):
    """ Returns an array of ratio values for number of male nodes and female nodes
    """
    df["ratio"] = df.apply(lambda x: get_ratio(x, typ), axis=1)
    df = df.sort_values("file")
    ratio = df.ratio.values
    return ratio



def get_unidirectional_links(D):
    R = nx.DiGraph()
    G = D.to_undirected()
    for (u, v) in D.edges():
        if not D.has_edge(v, u):
            R.add_edge(u,v)
    return R