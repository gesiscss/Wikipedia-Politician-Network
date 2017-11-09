import networkx as nx
from os import listdir
from os.path import isfile, join

# this has to be done with python 3.x

def get_files(path):
    """ Returns a list of files in a directory
        Input parameter: path to directory
    """
    mypath = path
    complete = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return complete

files = get_files("../data/filtered_graphs/")

for file in files:

	G = nx.read_gpickle("../data/filtered_graphs/"+file)
	nx.write_gpickle(G, file, protocol=2)