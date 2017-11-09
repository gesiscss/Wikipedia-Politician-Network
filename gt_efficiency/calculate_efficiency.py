import nx2gt
import networkx as nx
from burt_measure import efficiency
from graph_tool import *
import pandas as pd 

# nxG = nx.read_gpickle("2003_12_dir_dir")

	
# print(GraphView(G, vfilt = 'male'))

def get_id_efficiecy_df(path_nxGraph):
	""" Returns dictionaty with ID as KEY, and EFFICIENCY as VALUE
		Saves it as {year_month}_eff.csv 
	"""

	nxG = nx.read_gpickle(path_nxGraph)


	G = nx2gt.nx2gt(nxG)
	vprop = G.vertex_properties["id"]

	# fil = G.vertex_properties["gender"]
	lst = []
	for v in G.vertices():
		i_d = vprop[v]
		eff = efficiency(G,v)
		sub = [i_d,eff]
		lst.append(sub)

	df = pd.DataFrame(lst)
	df.columns = ['id', 'efficiency']

	path = "_".join([path_nxGraph.split("_")[0], path_nxGraph.split("_")[1],"eff.csv"])
	df.to_csv(path, index=False,encoding="utf-8")
	print("Saved at path: "+path)

	return df


# print(get_id_efficiecy_df("2003_12_dir_dir"))

# r= pd.DataFrame({
# 	'name': ['fajle1']
# 	})
# r.to_csv("files.csv", encoding="utf-8")

files = pd.read_csv("files.csv")['name'].values

for file in files: 
	get_id_efficiecy_df(file)