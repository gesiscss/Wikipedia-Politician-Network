from prepare_data import * 
import pandas as pd
import numpy as np
from datetime import datetime
from matplotlib import pyplot as plt
from itertools import groupby
from collections import Counter
import seaborn as sns
import sys
from os import listdir, sep
from os.path import isfile, join

def get_most_frequent(df, column_name, n):
	flat = [i for i in df[column_name].values if len(i)>0]
	flat = sum(flat, [])
	c = Counter(flat)
	if column_name == "occupation":
		return c.most_common(n+1)[1:]
	return pd.DataFrame(c.most_common(n))

def get_unique_values_multilevel_categorical(df, column_name):
	flat = [i for i in df[column_name].values if len(i)>0]
	flat = sum(flat, [])
	keys = Counter(flat).keys()
	return keys, len(keys)

# lst = ["occupation", "party", "nationality"]
def return_most_frequent(df,n,col):
	""" Prints top n most frequent values in every column from the passed list
	"""
	touple = get_most_frequent(df,col,n)
	lst = []
	for i in touple:
		lst.append(i[0])
	return lst

def extract_columns(df, nationality):
	# print("1",df.shape)
	df["party"] = df["party"].apply(lambda x: clean_lst(x))
	df = add_age(df)
	df = add_alive_status(df)
	df = add_distance(df)
	df = add_delta(df)
	df = add_lst_size(df,"nationality")
	df = add_lst_size(df,"party")
	df = add_lst_size(df,"occupation")

	# Dummyfy party column
	lst = []
	if nationality == "french":
		lst = ["union for a popular movement", "socialist party (france)","the republicans (france)","radical party (france)","rally for the republic"]
	if nationality == "british":
		lst = ["labour party (uk)","conservative party (uk)","ulster unionist party", "democratic unionist party"]
	if nationality == "russian":
		lst = ["communist party of the soviet union","united russia"]
	if nationality == "german":
		lst = ["social democratic party of germany","christian democratic union of germany","nazi party","socialist unity party of germany"]
	if nationality == "american":
		lst = ["democratic party (united states)","republican party (united states)"]

	party_abr_lst = []
	for party in lst:
		l = party.split(" ")
		p = ""
		for i in l:
			p += i[0]
		party_abr_lst.append(p)
		print(party)
		df = add_binary_column(df,"party",p,party)
	print(party_abr_lst)
	df["other_o"] = df.apply(lambda x: other_to_bin(x, party_abr_lst), axis=1)

	# print("4",df.shape)
	 # Dummyfy occupation column
	occ_lst = return_most_frequent(df,5,"occupation")
	
	occ_abr_lst = []
	for occ in occ_lst:
		l = occ.split(" ")
		p = ""
		for i in l:
			p += i[0]
		party_abr_lst.append(p)
		df = add_binary_column(df,"party",p,occ)


	df["other_o"] = df.apply(lambda x: other_to_bin(x, occ_abr_lst), axis=1)
	# print(df.shape)
	df['year_interval'] = pd.cut( df['entered'], [2000,2005,2010,2016], labels=[1,2,3])
	# print(df.shape)
	return df, occ_abr_lst, party_abr_lst


def main():
	global removeFromModel
	global removeFromModel_2


	files_path = sys.argv[1]
	print(files_path)
	path_save = sys.argv[2]
	print(path_save)
	nationality = sys.argv[3]
	print(path_save)
	
	# load the files 
	files = get_files(files_path)
	# df = pd.read_pickle("data/connected_sources/2016")
	for file in files:

		file_name = file.split(sep)[-1]
		print("Year:", file_name)
		# load the data 
		df = pd.read_pickle(file)

		df = filter_by_value(df, "nationality", nationality)

		df,occ_abr_lst,party_abr_lst = extract_columns(df, nationality)

		if "name_q" not in df.columns:
			remove_from_base.remove("name_q")
			removeFromModel.remove("name_q")
			removeFromModel_2.remove("name_q")

		model = drop_columns(df, removeFromModel)
		print("MODEL LARGE DF: ",model.shape)
		save_file(model, join(join(path_save,"model_large"),file_name+"_"+nationality))

		model2 = drop_columns(df, removeFromModel_2+occ_abr_lst+party_abr_lst)
		print("MODEL DF: ",model2.shape)
		save_file(model2, join(join(path_save,"model"),file_name+"_"+nationality))


# After removing these columns, a  MODEL DATAFRAME WILL BE LEFT
removeFromModel = ['#DBpURL', 'id', "ID", 'WikiURL', 'birthDate', 'deathDate', 'first_name',
			   'full_name', 'name', 'nationality', 'occupation', 'party','name_u',"name_q"]

# After removing these columns, a MODEL 2 DATAFRAME WILL BE LEFT
removeFromModel_2 = ['#DBpURL', 'id',"ID", 'WikiURL', 'birthDate', 'deathDate', 'first_name',
				'full_name', 'name', 'nationality', 'occupation', 'party','name_u', 'other_o',"name_q"] 

if __name__ == '__main__':
	main()