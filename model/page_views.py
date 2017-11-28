
# coding: utf-8

# In[91]:

import requests
import pandas as pd 
import json
import numpy as np
from datetime import datetime
import sys

endpoint = "https://wikimedia.org/api/rest_v1"


def return_url(article_name):
    """ Returns url for specified name
    """
    project = "en.wikipedia.org"
    access = "all-access"
    agent = "all-agents"
    article = article_name
    granularity = "monthly"
    start = "20010101"
    end = "20170101"
    params = "/metrics/pageviews/per-article/{}/{}/{}/{}/{}/{}/{}".format(project,access,
    agent, article, granularity, start, end)
    return params

def get_views(name): 
    """ Returns dictionary with monthly view numbers
    """
    headers = {'content-type': 'application/json'}
    r = requests.get(endpoint+return_url(name), headers = headers)
    resp_dict = json.loads(r.content.decode())
    return resp_dict

def cum_views(resp_dict, year):
    """ Retruns cumulative number of views for page in specified year
    """
    views = 0
    for dic in resp_dict['items']:
        if dic['timestamp'][:4] == str(year):
            views += dic['views']
    return views

# data = pd.read_json("../data/politicians_with_gender.json")

# data["url_name"] = data["WikiURL"].apply(lambda x: x.split("/wiki/")[1])


# names_df = data[["ID", "url_name"]]
# len(names_df)

# df1, df2, df3, df4 = np.array_split(names_df, 4)

# df1.to_csv("set1.csv", index=False, encoding="utf-8")
# df2.to_csv("set2.csv", index=False, encoding="utf-8")
# df3.to_csv("set3.csv", index=False, encoding="utf-8")
# df4.to_csv("set4.csv", index=False, encoding="utf-8")

if __name__ == '__main__':

    path = sys.argv[1]
    save = sys.argv[2]

    names = pd.read_csv(path)["url_name"].values

    count = 1
    lst = []
    for name in names:
        dic = get_views(name)
    #     print(cum_views(dic, 2016))
        sublst = [name, dic]
        lst.append(sublst)
        print("{} - {} - {}".format(count ,datetime.now(), name))
        count = count + 1


    df = pd.DataFrame(lst)
    df.to_json(save)
    print("Data saved at: "+save)
    



