# coding: utf-8

import pandas as pd 
import networkx
import pickle
from os import listdir
from os.path import isfile, join
from shutil import copyfile
import sys

def get_files(path):
    """ Returns a list of files in a directory
        Input parameter: path to directory
    """
    mypath = path
    complete = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return complete

def filter_files(interval):
    """ Returns filtered list of files 
        Input parameter: interval ("4m", "6m", "12m")
    """
    if interval == "4m":
        return [file for file in files if file.endswith("_01.csv") or file.endswith("_04.csv") or 
                file.endswith("_08.csv") or file.endswith("_12.csv")]
    if interval == "6m":
        return [file for file in files if file.endswith("_06.csv") or file.endswith("_12.csv")]
    if interval == "12m":
        return [file for file in files if file.endswith("_01.csv")]


def number_of_files(file_lst):
    """ Returns number of files 
        Input parameter: list of files
    """
    return len(file_lst)


def copy_files(files, path_copy, path_paste):
    """ Copies a list of files from location A to location B
        Input parameters:
        1. files - list of files
        2. path_copy - directory from which the data should be copied 
        3. path_paste - directory in which the data should be pasted
    """
    for file in files:
        copyfile(path_copy+"/"+file, path_paste+"/"+file)
    print("Files successfully copied!")


if __name__ == "__main__":

        path_copy = sys.argv[1]
        path_paste = sys.argv[2]
        interval = sys.argv[3]

        files = get_files(path_copy)
        files = filter_files(interval)
        print(files)
        print("Number of files:",number_of_files(files))
        copy_files(files, path_copy,path_paste)
