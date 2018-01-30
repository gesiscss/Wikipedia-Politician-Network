
# coding: utf-8

# In[1]:

import requests
from bs4 import BeautifulSoup
import pandas as pd
import cProfile
import wget
import gzip
import urllib
import zipfile
from io import StringIO
import smart_open
import sys
from tqdm import tqdm
import time
import random

host_path = "https://dumps.wikimedia.org/other/pagecounts-raw/"

#list of years to loop over: 2008-2014
years = range(2008,2015)
#list of months to loop over: 01 - 12
months = ["%.2d" % i for i in range(1, 13)]
# month[-1]

# example of forming url:
def form_url(year, month,file_name=""):
    """ Returns url for specified year and month
    """
    return host_path+str(year)+"/"+str(year)+"-"+str(month)+"/"+file_name
form_url(2008,'01')

# url = host_path+str(year[0])+"/"+str(year[0])+"-"+str(month[0])

def get_files(url):
    """ Returns all files from given url as a list
    """
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content,"html.parser")
    list_elements = soup.find_all("li")
    size = [li.text.split(" ")[-1].replace("M","") for li in list_elements]
#     print(size)
    list_elements = [li.a.get("href") for li in list_elements]
    return list_elements, size

# file_name = "pagecounts-20140701-040000.gz"
# save_path = "files/"

def download(file_name, save_path, lib="wget"):
    """ Downloads .gz file using the specified library and saves it on the specified path
    """
    # extract date information from file name and construct a url
    date = file_name.split("-")[1]
    year = date[:4]
    month = date[4:6]
    url = form_url(year, month, file_name)
    # print(url)
    # saving location
    save = save_path+"/"+file_name
    
    if lib == "wget":
            wget.download(url, save)
    if lib == "requests": 
        response = requests.get(url, stream=True)
        save = save_path+"/"+file_name
        handle = gzip.open(save, "wb")
        for chunk in response.iter_content(chunk_size=512):
#             if chunk:  # filter out keep-alive new chunks
                handle.write(chunk)
    if lib == "urllib":
        testfile = urllib.request.urlretrieve(url,save)
    if lib == "smart_open":
        handle = gzip.open(save, "wb")
        for line in smart_open.smart_open(url):
            handle.write(line)

# ## Requests

# In[24]:

# cProfile.run('download(file_name, save_path, "requests")')


# # Wget

# In[25]:

# cProfile.run('download(file_name, save_path)')


# ## Urllib

# In[26]:

# cProfile.run('download(file_name, save_path, "urllib")')


# # Smart Open

# In[27]:

# cProfile.run('download(file_name, save_path, "smart_open")')


# # Total number of files to download

# In[28]:

# num_files = 0
# for year in years:
#     file_name = str(year)+".csv"
#     df = pd.read_csv(file_name)
#     num_files = num_files + len(df)
# print("Number of files to be downloaded {}".format(num_files))


# In[ ]:

if __name__ == '__main__':
    
    year_file = sys.argv[1]
    save_path = sys.argv[2]


    # load files for specified year 
    df = pd.read_csv(year_file)
    # print(df)    
    files = df["file"].values
    # print(files)

    #download one by one

    for count , file in enumerate(files):
        if count % 5 == 0:
                # print("sleeping start")
                time.sleep(random.uniform(1.0, 3.0))
                # print("wake up")
        if count % 25 == 0:
            print("Progress report: {} / {}".format(count, len(files)))
        download(file, save_path)


