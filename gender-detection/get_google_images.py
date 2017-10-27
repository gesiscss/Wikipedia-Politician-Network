
# coding: utf-8

# In[67]:

from bs4 import BeautifulSoup
import requests
import re
import os
import http.cookiejar
import json
import pandas as pd
from datetime import datetime


# In[14]:

def get_soup(url,header):
    resp = requests.get(url,headers=header)
    return BeautifulSoup(resp.content,'html.parser')


query = "Nikola+Tesla" # you can change the query for the image  here
image_type="ActiOn"
url="https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"
# print(url)
#add the directory for your image here
# DIR="Pictures"
header={
    'User-Agent':
    "Mozilla/5.0 (Windows NT 6.1; WOW64)AppleWebKit/537.36 (KHTML, like Gecko)Chrome/43.0.2357.134 Safari/537.36"
}
soup = get_soup(url,header)


# In[37]:

def get_soup(url,header):
    """ Returns beautiful soup object for specified url
    """
    resp = requests.get(url,headers=header)
    return BeautifulSoup(resp.content,'html.parser')


# In[17]:

# actual_images=[] 
# for a in soup.find_all("div",{"class":"rg_meta"})[:5]:
#     link = json.loads(a.text)["ou"]
# #     link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
#     actual_images.append((link))


# In[38]:

def get_url_list(soup, num): 
    """ Returns top 'num' image URLs
    """
    actual_images=[] 
    for a in soup.find_all("div",{"class":"rg_meta"})[:num]:
        link = json.loads(a.text)["ou"]
    #     link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
        actual_images.append((link))
    return actual_images


# In[35]:

# get_url_list(soup)


# In[29]:

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


# In[34]:

# names = load_list("full_names.csv","name")
# len(names)


# In[36]:

def get_query(name):
    """ Returns query url for specified name
    """
    return "https://www.google.co.in/search?q="+name+"&source=lnms&tbm=isch"


# In[113]:

# path = "full_names.csv"

def return_url_df(path, path_save):
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


# In[111]:

df = return_url_df(path, "test.csv")


# In[80]:

# pd.read_csv("C:/Users/vujovisn/Documents/dev/altmetrics-twitter/gender_detection/google_img/out_gend_formal.csv")


# In[ ]:



