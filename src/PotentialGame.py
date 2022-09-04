# -*- coding:utf8 -*-
import urllib2
import time
import pymongo
import json
import operator
from collections import OrderedDict

myclient = pymongo.MongoClient('mongodb://localhost:27017/')
myapp = myclient["steam"]['apps']
myreview = myclient["steam"]['reviews']

d = {}

for review in myreview.find( {"language":"english", "review":{"$regex":"fun"}}):
    app = myapp.find_one({"appid":review["appid"]})
    if "spy" in app and "price" in app["spy"] and app["spy"]["price"] == "0":
        continue
    if review["appid"] in d:
        d[review["appid"]] += 1
    else:
        d[review["appid"]] = 1
"""
with open ("./output.json", 'r') as ff:
    d = json.load(ff)
"""

t = {}
for k in d:
    app = myapp.find_one({"appid":int(k)})
    if "total_reviews" not in app:
        continue
    reviewNum = app["total_reviews"]
    if reviewNum > 100:
        c = d[k] *1.0 /reviewNum
        t[k] = c
    t[k] = d[k]


sorted_d = OrderedDict( sorted(t.items(), key=operator.itemgetter(1),reverse=True))

with open ("./output.json", 'w') as ft:
    json.dump(sorted_d, ft)
