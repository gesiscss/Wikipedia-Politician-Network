import numpy as np
import os 
import sys
import matplotlib.pylab as plt
# import dill
from collections import Counter,defaultdict
# from util import output_file_path_ssd, output_plot_path,output_file_path,flatten
from scipy import stats
# import cPickle
import matplotlib
from matplotlib import rc
import networkx as nx 
import pandas as pd 
import stats as stat
import operator


plt.rcParams['figure.dpi'] = 600
#plt.rcParams['font.size'] =25
plt.rcParams.update({'font.size': 25})
plt.rcParams['font.family'] = 'serif'
#plt.rcParams['figure.figsize'] = (6, 6)

#rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
#rc('font',**{'family':'serif','serif':['Times']})
#rc('font', family='sans-serif')
#rc('font', serif='Helvetica')
rc('text', usetex=True)
labels = {'male':'male' ,'female':'female'}
#colors = {'m':'#998ec3' ,'f':'#f1a340'}
colors = {'male':'#6858a7' ,'female':'#d58010'}
ls = {'male':'-' ,'female':'-'}
marker_style = {'male':'>' ,'female':'H'}
lw = 5
ms= 9

def nomalize_degree(per_gender_seq):
    '''
    normalize degree distribution by total number of nodes
    '''
    pk_g = {}
    for gender, seq in per_gender_seq.items():
        hist = Counter(seq)
        if 0 in hist:
            del hist[0]
        n = sum(hist.values())
        pk_g[gender] = {degree: freq/float(n) for degree,freq in hist.items()}
    return pk_g 

def get_xy(data):
    pk_g = nomalize_degree(data)
    r = {}
    for gender, hist in pk_g.items():
        sorted_pk = sorted(hist.items(), key=operator.itemgetter(0),reverse=True)
        x = [i[0] for i in sorted_pk]
        y = np.cumsum([i[1] for i in sorted_pk])
        r[gender] = (x,y)
    return r

def hist(degree,kcore,clust,fpath=None,text=None):
    '''
    plot the degree distribution for:
    1) per gender
    2) whole graph
    '''

    fmt = matplotlib.ticker.StrMethodFormatter("{x}")
    fig,ax = plt.subplots()
    
    left, bottom, width, height = [0.70, 0.65, 0.25, 0.25]
    ax2 = fig.add_axes([left, bottom, width, height])
    
    left, bottom, width, height = [0.23, 0.25, 0.25, 0.25]
    ax3 = fig.add_axes([left, bottom, width, height])
#

    for  gender , xy in get_xy(degree).items():
        x,y = xy
        l = ax.plot(x,y, ls[gender],color=colors[gender],label=labels[gender],lw=5,)
    ax.set_xlabel(r'Degree (d)',fontsize=33)
    ax.set_ylabel(r'P(x $\geq$ d)',fontsize=33)
    


    for  gender , xy in get_xy(kcore).items():
        x,y = xy
        a = ax2.plot(x,y , ls[gender],color=colors[gender],label=labels[gender],lw=4.,)
    
    ax2.set_xlabel(r'k-core (k)',fontsize=20)
    ax2.set_ylabel(r'P(x $\geq$ k)',fontsize=20)
    xlabels = ax2.get_xticklabels()
    for label in xlabels:
        label.set_rotation(90) 

    for gender, xy in get_xy(clust).items():
        x,y = xy
        a = ax3.plot(x,y, ls[gender],color=colors[gender],label=labels[gender],lw=4.,)
    xlabels = ax3.get_xticklabels()
    for label in xlabels:
        label.set_rotation(90) 

    ax3.set_xlabel(r'efficiency (e)',fontsize=20)
    ax3.set_ylabel(r'P(x $\geq$ e)',fontsize=20)
    

    degree_xlim=(0,1e+3)
    degree_ylim=(1e-6,1)
    
    ax2.set_yscale('log') 
    ax.set_yscale('linear') 
    ax.set_xscale('log') 
    ax3.set_xscale('log') 
    ax2.set_xscale('log') 
    
    
    ax.set_ylim(degree_ylim)
    
    ax.tick_params(direction='out')
    ax.spines["top"].set_visible(False)  
    ax.spines["right"].set_visible(False) 
    ax.get_xaxis().tick_bottom()  
    ax.get_yaxis().tick_left()
#    
    ax2.tick_params(direction='out')
    ax2.spines["top"].set_visible(False)  
    ax2.spines["right"].set_visible(False) 
    ax2.get_xaxis().tick_bottom()  
    ax2.get_yaxis().tick_left()

    
    ax3.tick_params(direction='out')
    ax3.spines["top"].set_visible(False)  
    ax3.spines["right"].set_visible(False) 
    ax3.get_xaxis().tick_bottom()  
    ax3.get_yaxis().tick_left()
    
    ax.xaxis.set_tick_params(labelsize=30)
    ax2.yaxis.set_tick_params(labelsize=20)
    ax2.xaxis.set_tick_params(labelsize=20)
    ax3.yaxis.set_tick_params(labelsize=20)
    ax3.xaxis.set_tick_params(labelsize=20)
    t = r'{0}'.format(text) 
    bbox={"boxstyle":'round,pad=0.2','facecolor':'white',"lw":2,"ec":"#66c2a5"}

    ax.text(0.04, -0.175, t,verticalalignment='bottom', horizontalalignment='left',
            transform=ax.transAxes, color= 'grey', fontsize=25., weight='bold',bbox=bbox)
    
    ax2.tick_params(direction='out')
    ax2.spines["top"].set_visible(False)  
    ax2.spines["right"].set_visible(False) 
    ax2.get_xaxis().tick_bottom()  
    ax2.get_yaxis().tick_left()
    y = int(text) 
    # print fpath

    # plt.show()

    plt.savefig(fpath,bbox_inches='tight')
    
plt.close('all')

g = nx.read_gpickle("data/graphs_sats/2016_12_dir_dir")

mg = stat.filter_graph(g,"gender","male")
fg = stat.filter_graph(g,"gender","female")
        # in_deg = nx.get_node_attributes(fg,'in_degree')
        # tp = (('female', nx.get_node_attributes(fg,'in_degree')), ('male', nx.get_node_attributes(mg,'in_degree')))
        # print(tuple(nx.get_node_attributes(fg,'in_degree')))
dic = {}
dic['female'] = nx.get_node_attributes(fg,'in_degree')
dic['male'] = nx.get_node_attributes(mg,'in_degree')
k_core = {}
k_core['female'] = nx.get_node_attributes(fg,'k_core')
k_core['male'] = nx.get_node_attributes(mg,'k_core')
d_degree = dic
d_kcore =  k_core
efficiency = d_kcore
hist(d_degree,d_kcore,efficiency,"testtt.png",text='2016_12')