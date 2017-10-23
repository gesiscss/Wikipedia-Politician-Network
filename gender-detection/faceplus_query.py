#!/usr/bin/perl
from __future__ import print_function
import urllib2
import simplejson
from urllib2 import *
#import pandas as pd
import json
import os.path
import string
import time
import random
import csv
import sys


def infering_gender(author_name, url_list, path_write):

    #-------------------------------------------------------------------------
    # ANALYZE PICS
    #-------------------------------------------------------------------------
    # api_secret='YQxKgp0cc_9_7VrpNVvOzvHcrAKyT9Tf%20'
    # api_key='bc789832efda15a47561499b9c048677'

    # https://apius.faceplusplus.com/v2/detection/detect?url=http://upload.wikimedia.org/wikipedia/commons/7/71/07.05-A-0025.jpg&api_secret=YQxKgp0cc_9_7VrpNVvOzvHcrAKyT9Tf%20&api_key=bc789832efda15a47561499b9c048677&attribute=glass,pose,gender,age,race,smiling

    API_SECRET = "YQxKgp0cc_9_7VrpNVvOzvHcrAKyT9Tf%20"
    API_KEY = "bc789832efda15a47561499b9c048677"

    for url in url_list:
        url = url.replace("u'", "'")
        url = url.strip('[')
        url = url.strip(']')
        url = url.replace("'", '')
        apiurl = "https://apius.faceplusplus.com/v2/detection/detect?url="
        apiurl += url
        apiurl += "&api_secret=" + API_SECRET + "&api_key=" + \
            API_KEY + "&attribute=glass,pose,gender,age,race,smiling"

        request = Request(apiurl)
        request.add_header('User-agent', 'Mozilla/5.0 (Linux i686)')
        try:
            response = urlopen(request)
        except HTTPError:
            continue
        data = json.load(response)
        try:
            file = open(str(path_write), 'a')
            # file.write(author_name)
            json.dump([author_name, data], file)
            file.write('\n')
            file.close()
        except IOError as e:
            log.write(urlid)


# print("Prosao")
if __name__ == "__main__":

    path_read = sys.argv[1]
    path_write = sys.argv[2]

    fileName = str(path_read)
    #line_count = 0
    #interupted_line = 104
    with open(fileName, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, skipinitialspace=True)
        for row in spamreader:
            #line_count += 1

            # if line_count > interupted_line:
            # print("usao u IF")
            name = row[0]
            url_list = row
            url_list.remove(name)
            print(name)
            infering_gender(name, url_list,path_write)
    # with open('output.csv','rb') as csvfile:
    #     print(csv.reader(csvfile,skipinitialspace=True))
    #     for r in csv.reader(csvfile,skipinitialspace=True):
    #         print(r)


# print('prosao')
