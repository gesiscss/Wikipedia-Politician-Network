
# coding: utf-8

import wikipedia
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import tqdm
import requests
import urllib
import warnings
warnings.filterwarnings('ignore')
# get_ipython().magic('matplotlib inline')

data = pd.read_pickle("data/connected_sources/2016")


def extract_size(url, name):
    r = requests.get(url.format(urllib.parse.quote(name)))
    pid = list(r.json()['query']['pages'].keys())[0]
    print(pid)
    p = wikipedia.page(pageid=pid)
    return len(p.content.replace("\n", "").replace("==","").strip(" ").split(" "))

def get_article_size(name):
    """ Returns number of words per article
    """
#     wiki_url = x["WikiURL"]
    url = "https://en.wikipedia.org/w/api.php?action=query&titles={}&format=json"
    page = ""
    try:
        page = wikipedia.page(name)
    except:
        print(name)
        try:
            return extract_size(url, name)
        except:
            return 0 
    return len(page.content.replace("\n", "").replace("==","").strip(" ").split(" "))

# d = data.head(500)
# d['article_size'] = d["name_u"].apply(lambda x: get_article_size(x))

# sns.regplot("article_size", "views", d)

# data = data.head(100)
data['article_size'] = data["name_u"].apply(lambda x: get_article_size(x))

data[['id','article_size']].to_csv("data/article_length/length_2018.csv")





