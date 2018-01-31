from multiprocessing import Queue, Pool
import concurrent.futures
import random
import time
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
from functools import partial

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
 
# def f(x):
#     if random.randint(0,1):
#         time.sleep(0.1)
#     #
#     res = x * x
#     q.put(res)

def download(file_name, save_path, lib="requests"):
    """ Downloads .gz file using the specified library and saves it on the specified path
    """
    # extract date information from file name and construct a url
    time.sleep(random.uniform(0.1, 0.5))
    date = file_name.split("-")[1]
    year = date[:4]
    month = date[4:6]
    url = form_url(year, month, file_name)
    # print(url)
    # saving location
    count = 0
    save = save_path+"/"+file_name
    
    if lib == "wget":
        wget.download(url, save)
    if lib == "requests": 
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            save = save_path+"/"+file_name
            handle = gzip.open(save, "wb")
            for chunk in response.iter_content(chunk_size=1024):
    #             if chunk:  # filter out keep-alive new chunks
                    handle.write(chunk)
        else:
            if count <= 2:
                count = count +1
                time.sleep(random.uniform(1.0,2.0))
                download(file_name, save_path, lib="requests")
            else:
                print("Doesn't download: "+file_name)
                return 
    if lib == "urllib":
        testfile = urllib.request.urlretrieve(url,save)
    if lib == "smart_open":
        handle = gzip.open(save, "wb")
        for line in smart_open.smart_open(url):
            handle.write(line)
    q.put(url)
 
def main():

    year_file = sys.argv[1]
    save_path = sys.argv[2]

    # load files for specified year 
    df = pd.read_csv(year_file)
    # df = df.sort_value             
    # print(df)    
    files = df["file"].values
 
    q = Queue()

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        for file in files:
            executor.submit(download, file, save_path, lib="wget")
    #
    while not q.empty():
        print("Done: ", q.get())
    # with Pool(2) as p:
    #     # records = p.starmap(download, files, save_path)
    #     records = p.map(partial(download, save_path=save_path), files)
    #     print(records)
if __name__ == '__main__':
    main()