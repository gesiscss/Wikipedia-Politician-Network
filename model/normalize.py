from sklearn import preprocessing
from sklearn.feature_selection import f_regression, mutual_info_regression, SelectKBest, RFE, VarianceThreshold
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn import linear_model
import scipy.stats as stats
import pandas as pd 
import numpy as np 
from numpy import inf
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from collections import Counter

def zscore_wikipedia_entered(data_frame, columns):
	"""
	Normalizing column values based on mean and std of articles with same Wikipedia age
	:param data_frame: A pandas DataFrame to be processed
	:param columns: List of column names of categorical variables 
	:returns data_frame: DataFrame with normalizedcolumns
	"""    
	data_frame = data_frame.reset_index()
	for col in columns:
		for enter in data_frame["entered"].unique():
			temp = data_frame[data_frame["entered"]==enter]
			mean = np.mean(temp[col].values)
			std = np.std(temp[col].values)
			temp[col] = (temp[col] - mean)/std
			#print(stats.zscore(temp[col].values))
			data_frame.update(temp[col])
		
	return data_frame

def normalize(data_frame, columns):
	"""
	Normalizing (loged) column values
	:param data_frame: A pandas DataFrame to be processed
	:param columns: List of column names of categorical variables 
	:returns data_frame: DataFrame with normalizedcolumns
	"""    
	for col in columns:
		#data_frame[col] = log_colum_values(data_frame[col])
		#square root is also defined for negative values
		data_frame[col] = np.sqrt(data_frame[col])
	return data_frame

def log_colum_values(series_col):
	"""
	Normalizing (loged) column values
	:param series: Column of dataframe 
	:returns np array: DataFrame with normalizedcolumns
	"""    
	min_val = series_col.min()
	values = [log_value(v, np.abs(min_val))for v in series_col.values]
	return values

def log_value(x, min_val):
	"""
	Logs a value, replacing -inf with 0 and handling negative values
	:param x: value
	:param min_val: min value in list 
	:returns value: loged numerical value
	"""    
	#shift data to positive values
	x = x + min_val
	if x>0:
		return np.log(x)
	else:
		print("ERROR log_value: shifting data was not working")
	#if np.log(x) == -inf:
	#    return 0 
	#if x < 0:
	#         print("na")
	#    return np.log(x + 1 - min_val)

def plot_loged(data, col_name):
	min_val = series_col.min()
	data[col_name] = [(v + np.abs(min_val)) for v in data[col_name]]   
	x= np.log(data[col_name])
	#x = x[~np.isnan(x)]
	#x = x[x != np.inf]
	#x = x[x != -np.inf]
	sns.distplot(x)

def plot_square_root(data, col_name):
	x= np.sqrt(data[col_name])
	sns.distplot(x)

