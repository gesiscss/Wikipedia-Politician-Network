import threading
import requests
import gzip
import sys
import pandas as pd
import wget
import time
import random
import cProfile

# global
next_run = []

def download(url, save_path, lib="requests"):
    """ Downloads file to specified path, if server returns status codes other than 200 url is saved
    """
    # the speed diference is insignificant between 'requests' and 'wget'
    global next_run

    f_name = url.split("/")[-1]
    save = save_path+"/"+f_name

    if lib == "requests":
        
        r = requests.get(url, stream=True)
        if r.status_code != 200:
            next_run.append(url)
            print("Added {} to NEW ROUND (bach size: {})".format(f_name, len(next_run)))
            
        with open(save, 'wb') as f:
            for chunk in r.iter_content(1024):
                if chunk:
                    f.write(chunk)

    if lib == "wget":
        try:
            wget.download(url, save)
        except:
            next_run.append(url)
            print("Added {} to NEW ROUND (bach size: {})".format(f_name, len(next_run)))
    # wget.download(url, save)

def createNewDownloadThread(url, save_path):
    """ Creates download thread
    """
    global next_run
    download_thread = threading.Thread(target=download, args=(url,save_path))
    download_thread.start()


def scrape(urls, save_path):
    """ Tries to download files from the urls list and starts a thread for each of them
    """
    for count, url in enumerate(urls):
        time.sleep(random.uniform(1.0, 2.0))
        if count % 10 == 0 and count != 0:
            time.sleep(random.uniform(2.0, 8.0))
        print(url)
        createNewDownloadThread(url, save_path)

def main():
    global next_run
    year_file = sys.argv[1]
    save_path = sys.argv[2]

    df = pd.read_csv(year_file)
    # df = df.sort_value             
    # print(df)    
    urls = list(df["url"].values)

    scrape(urls,save_path)

    counter = 1
    while len(next_run) != 0:
        time.sleep(10)
        print("--------------------------------- ------------- ----------------------------------")
        print("--------------------------------- NEW RUN    {} ----------------------------------".format(counter))
        print("--------------------------------- BATCH SIZE {} ----------------------------------".format(len(next_run)))

        urls = next_run
        next_run = []
        scrape(urls, save_path)
        counter = counter +1


if __name__ == '__main__':
    cProfile.run('main()') 
    # main()
