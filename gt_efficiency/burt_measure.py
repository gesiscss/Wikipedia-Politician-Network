import os
import sys
import dill

import graph_tool.all as gt

def efficiency(G,v):
    neighbours = list(v.all_neighbours())
    n = float(len(neighbours))
    r = []
    for vn in neighbours:
        temp =  list(vn.all_neighbours())
        common_nodes = set(neighbours) & set(temp) #-1 for removing the count for the EGO node
        redundancies = len(common_nodes)
        r.append(redundancies/n)
    effective_size = n - sum(r) 
    if n==0:
        return 0 
    else:
        return effective_size/n
 
if __name__ == '__main__':
pass 