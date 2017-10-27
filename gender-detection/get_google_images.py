
# coding: utf-8

# In[67]:

from bs4 import BeautifulSoup
import requests
import re
import os
# import http.cookiejar
import json
import pandas as pd
from datetime import datetime
import sys

def get_soup(url,header):
    """ Returns beautiful soup object for specified url
    """
    resp = requests.get(url,headers=header)
    return BeautifulSoup(resp.content,'html.parser')


def get_url_list(soup, num): 
    """ Returns top 'num' image URLs
    """
    actual_images=[] 
    for a in soup.find_all("div",{"class":"rg_meta"})[:num]:
        link = json.loads(a.text)["ou"]
    #     link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
        actual_images.append((link))
    return actual_images


def load_list(path,col,typ="csv"):
    """ Returns list of unique names 
    """
    if typ == "csv":
        df = pd.read_csv(path)
        return df[col].unique()
    if typ == "json":
        df = pd.read_json(path)
        return df[col].unique()
    return []


def get_query(name):
    """ Returns query url for specified name
    """
    return "https://www.google.co.in/search?q="+name+"&source=lnms&tbm=isch"


def return_url_df(path, path_save):
    """ Returns dataframe with 5 urls for each name, and each url is a value in one column
    """
    names = load_list(path, "name")
    print(str(len(names))+" names loaded!")
#     lst = list(names)

    header={
        'User-Agent':
        "Mozilla/5.0 (Windows NT 6.1; WOW64)AppleWebKit/537.36 (KHTML, like Gecko)Chrome/43.0.2357.134 Safari/537.36"
    }

    url1, url2, url3, url4, url5 = [],[],[],[],[]
    num = 1
    for name in names:
        url = get_query(name)
        soup = get_soup(url, header)
        link1, link2, link3, link4, link5 = get_url_list(soup,5)
        url1.append(link1)
        url2.append(link2)
        url3.append(link3)
        url4.append(link4)
        url5.append(link5)
        
        print("{} - {} - {}".format(num, str(datetime.now()), name))
        
        num = num + 1
#         print(len(url1), len(url2), len(url3), len(url4), len(url5))
    df = pd.DataFrame({
        'name': names,
        'url1':url1,
        'url2':url2,
        'url3':url3,
        'url4':url4,
        'url5':url5
    })
    
    df.to_csv(path_save, header=False, index=False, encoding="utf-8")
    print("Dataframe saved at: "+path_save)
    return df


if __name__ == "__main__":

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    df = return_url_df(input_path, output_path)






